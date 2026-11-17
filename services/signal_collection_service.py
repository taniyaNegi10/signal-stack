
import hashlib
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

from database import get_connection


class SignalCollectionService:

    USER_AGENT = "SignalStackResearchBot/1.0"
    MAX_CONTENT_LENGTH = 5000

    def collect_signals(self, company_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, url, category
            FROM sources
            WHERE company_id = ? AND approved = 1
        """, (company_id,))

        sources = cursor.fetchall()
        conn.close()

        results = {
            "company_id": company_id,
            "sources_checked": len(sources),
            "signals_saved": 0,
            "duplicates_skipped": 0,
            "failed_sources": [],
            "signals": []
        }

        for source in sources:
            source_id = source["id"]
            source_name = source["name"]
            url = source["url"]
            category = source["category"]

            try:
                page = self._fetch_page(url)

                if not page:
                    results["failed_sources"].append({
                        "source": source_name,
                        "reason": "Page could not be fetched or access was not permitted."
                    })
                    continue

                title, content = page

                if not title and not content:
                    results["failed_sources"].append({
                        "source": source_name,
                        "reason": "No meaningful page content found."
                    })
                    continue

                content_hash = hashlib.sha256(
                    f"{url}|{title}|{content}".encode("utf-8")
                ).hexdigest()

                saved = self._save_signal(
                    company_id=company_id,
                    source_id=source_id,
                    title=title or source_name,
                    content=content,
                    category=category,
                    source_url=url,
                    content_hash=content_hash
                )

                if saved:
                    results["signals_saved"] += 1
                    results["signals"].append({
                        "title": title or source_name,
                        "category": category,
                        "source_url": url
                    })
                else:
                    results["duplicates_skipped"] += 1

            except Exception as error:
                results["failed_sources"].append({
                    "source": source_name,
                    "reason": str(error)
                })

        return results

    def _fetch_page(self, url):
        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            return None

        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

        parser = RobotFileParser()
        parser.set_url(robots_url)

        try:
            robots_response = requests.get(
                robots_url,
                headers={"User-Agent": self.USER_AGENT},
                timeout=10
            )

            if robots_response.status_code in (401, 403):
                return None

            if robots_response.status_code == 404:
                parser.parse([])
            elif robots_response.ok:
                parser.parse(robots_response.text.splitlines())
            else:
                return None

        except requests.RequestException:
            return None

        if not parser.can_fetch(self.USER_AGENT, url):
            return None

        response = requests.get(
            url,
            headers={"User-Agent": self.USER_AGENT},
            timeout=15
        )

        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "").lower()

        if "text/html" not in content_type:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        for element in soup([
            "script", "style", "nav", "footer",
            "header", "form", "noscript"
        ]):
            element.decompose()

        title = soup.title.get_text(" ", strip=True) if soup.title else ""

        main_content = soup.find("main") or soup.find("article") or soup.body

        if not main_content:
            return None

        content = main_content.get_text(" ", strip=True)
        content = " ".join(content.split())

        return title, content[:self.MAX_CONTENT_LENGTH]

    def _save_signal(
        self,
        company_id,
        source_id,
        title,
        content,
        category,
        source_url,
        content_hash
    ):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT OR IGNORE INTO signals (
                    company_id,
                    source_id,
                    title,
                    content,
                    category,
                    impact,
                    relevance_score,
                    source_url,
                    content_hash
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                company_id,
                source_id,
                title,
                content,
                category,
                "Needs assessment",
                0,
                source_url,
                content_hash
            ))

            saved = cursor.rowcount > 0
            conn.commit()

            return saved

        finally:
            conn.close()
