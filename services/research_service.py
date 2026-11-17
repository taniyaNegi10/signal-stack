
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser


class ResearchService:

    USER_AGENT = "SignalStackResearchBot/1.0"

    def _check_robots_permission(self, url):
        """Check whether our crawler may access the requested URL."""

        parsed_url = urlparse(url)

        if parsed_url.scheme not in ("http", "https") or not parsed_url.hostname:
            return False, "Invalid or unsupported URL."

        robots_url = (
            f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
        )

        try:
            response = requests.get(
                robots_url,
                timeout=10,
                headers={"User-Agent": self.USER_AGENT}
            )

            # No published robots file: no rules are available.
            if response.status_code == 404:
                return True, "No robots.txt file published."

            # Do not crawl when access rules cannot be read.
            if response.status_code in (401, 403):
                return False, "Access to robots.txt is restricted."

            response.raise_for_status()

            parser = RobotFileParser()
            parser.set_url(robots_url)
            parser.parse(response.text.splitlines())

            allowed = parser.can_fetch(self.USER_AGENT, url)

            if not allowed:
                return False, "Crawling is disallowed by robots.txt."

            return True, "Crawling permitted by robots.txt."

        except requests.RequestException as error:
            return False, f"Could not verify robots.txt: {error}"

    def research_website(self, url):
        """Extract basic public website information when crawling is permitted."""

        allowed, permission_message = self._check_robots_permission(url)

        if not allowed:
            return {
                "url": url,
                "status": "blocked",
                "error": permission_message,
                "headings": []
            }

        try:
            response = requests.get(
                url,
                timeout=15,
                headers={"User-Agent": self.USER_AGENT}
            )

            response.raise_for_status()

            content_type = response.headers.get("Content-Type", "").lower()

            if "text/html" not in content_type:
                return {
                    "url": url,
                    "status": "failed",
                    "error": "The URL did not return an HTML page.",
                    "headings": []
                }

            soup = BeautifulSoup(response.text, "html.parser")

            title = (
                soup.title.get_text(strip=True)
                if soup.title
                else "Title not found"
            )

            meta_description = soup.find(
                "meta",
                attrs={"name": "description"}
            )

            description = (
                meta_description.get("content", "").strip()
                if meta_description
                else "Description not found"
            )

            headings = []
            seen_headings = set()

            for tag in soup.find_all(["h1", "h2", "h3"]):
                text = " ".join(tag.get_text(" ", strip=True).split())
                normalized_text = text.lower()

                if text and normalized_text not in seen_headings:
                    seen_headings.add(normalized_text)

                    headings.append({
                        "tag": tag.name,
                        "text": text
                    })

            return {
                "url": url,
                "title": title,
                "description": description,
                "headings": headings,
                "status": "success",
                "permission": permission_message
            }

        except requests.RequestException as error:
            return {
                "url": url,
                "status": "failed",
                "error": str(error),
                "headings": []
            }
