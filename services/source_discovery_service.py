
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
from urllib.robotparser import RobotFileParser


class SourceDiscoveryService:

    USER_AGENT = "SignalStackResearchBot/1.0"
    MAX_DISCOVERED_LINKS = 50

    SOURCE_CANDIDATES = [
        {
            "name": "MeetUniversity Student Testimonials",
            "url": "https://www.meetuniversity.com/",
            "category": "Customers",
            "reason": (
                "Contains student testimonials. These are "
                "first-party promotional statements, not independent reviews."
            )
        },
        {
            "name": "Meet My Uni",
            "url": "https://meetmyuni.com/",
            "category": "Competitors",
            "reason": (
                "Potential study-abroad competitor. Its current "
                "website content must be verified before approval."
            )
        },
        {
            "name": "University Grants Commission",
            "url": "https://www.ugc.gov.in/",
            "category": "Market",
            "reason": (
                "Official higher-education information relevant "
                "to the Indian education market."
            )
        },
        {
            "name": "Press Information Bureau",
            "url": "https://www.pib.gov.in/",
            "category": "Market",
            "reason": (
                "Government announcements and policy updates "
                "relevant to higher education."
            )
        },
        {
            "name": "Indian Express Education News",
            "url": "https://indianexpress.com/section/education/",
            "category": "Market",
            "reason": (
                "News coverage of education trends and study-abroad "
                "developments."
            )
        }
    ]

    PARKED_KEYWORDS = [
        "parked domain",
        "domain for sale",
        "buy this domain",
        "domain is parked",
        "hosting default page"
    ]

    IGNORED_EXTENSIONS = (
        ".jpg", ".jpeg", ".png", ".gif", ".svg",
        ".pdf", ".zip", ".mp4", ".mp3", ".webp",
        ".css", ".js", ".xml", ".ico"
    )

    def _get_robots_parser(self, website_url):

        parsed = urlparse(website_url)

        robots_url = (
            f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        )

        response = requests.get(
            robots_url,
            timeout=10,
            headers={"User-Agent": self.USER_AGENT}
        )

        # A missing robots.txt means no published rules.
        if response.status_code == 404:
            parser = RobotFileParser()
            parser.parse([])
            return parser

        # Do not crawl when access is forbidden or unavailable.
        if response.status_code in (401, 403):
            raise PermissionError(
                "Robots.txt access is restricted."
            )

        response.raise_for_status()

        parser = RobotFileParser()
        parser.set_url(robots_url)
        parser.parse(response.text.splitlines())

        return parser

    def _normalize_url(self, url):

        parsed = urlparse(url)

        clean_url = urlunparse((
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            parsed.path.rstrip("/"),
            "",
            parsed.query,
            ""
        ))

        return clean_url

    def check_source(self, source):

        result = source.copy()

        try:
            response = requests.get(
                source["url"],
                timeout=15,
                allow_redirects=True,
                headers={
                    "User-Agent": self.USER_AGENT
                }
            )

            result["status_code"] = response.status_code
            result["final_url"] = response.url

            response.raise_for_status()

            content_type = response.headers.get(
                "Content-Type", ""
            )

            if "html" not in content_type.lower():
                result["status"] = "not_html"
                result["error"] = "URL did not return HTML."
                return result

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            title = (
                soup.title.get_text(strip=True)
                if soup.title else ""
            )

            page_text = soup.get_text(
                separator=" ",
                strip=True
            )

            combined_text = (
                title + " " + page_text[:3000]
            ).lower()

            result["verified_title"] = (
                title if title else "Title not found"
            )

            if any(
                keyword in combined_text
                for keyword in self.PARKED_KEYWORDS
            ):
                result["status"] = "parked_domain"
                result["error"] = "Parked or placeholder domain."

            elif len(page_text.strip()) < 100:
                result["status"] = "needs_review"
                result["error"] = (
                    "Very little readable page content."
                )

            else:
                result["status"] = "accessible"
                result["error"] = None

        except requests.HTTPError as error:

            status_code = (
                error.response.status_code
                if error.response is not None
                else None
            )

            if status_code == 403:
                result["status"] = "blocked"
                result["error"] = (
                    "Automated request was blocked."
                )
            else:
                result["status"] = "http_error"
                result["error"] = str(error)

        except requests.RequestException as error:

            result["status"] = "unavailable"
            result["error"] = str(error)

        return result

    def discover_sources(self):

        discovered_sources = []

        for source in self.SOURCE_CANDIDATES:
            result = self.check_source(source)
            discovered_sources.append(result)

        return discovered_sources

    def discover_website_links(self, website_url):
        """Discover permitted, same-domain public HTML links."""

        try:
            # Check the website's published crawling rules first.
            robots = self._get_robots_parser(website_url)

            if not robots.can_fetch(
                self.USER_AGENT,
                website_url
            ):
                return {
                    "status": "blocked_by_robots",
                    "total_links": 0,
                    "links": [],
                    "error": (
                        "The website's robots.txt does not permit "
                        "crawling this page."
                    )
                }

            response = requests.get(
                website_url,
                timeout=15,
                headers={
                    "User-Agent": self.USER_AGENT
                }
            )

            response.raise_for_status()

            content_type = response.headers.get(
                "Content-Type", ""
            )

            if "html" not in content_type.lower():
                return {
                    "status": "failed",
                    "total_links": 0,
                    "links": [],
                    "error": "Website did not return HTML."
                }

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            base_host = (
                urlparse(response.url).hostname or ""
            ).lower()

            # Treat www.example.com and example.com as the same host.
            base_host = base_host.removeprefix("www.")

            discovered_links = []
            seen_urls = set()
            skipped_by_robots = 0

            for link in soup.find_all("a", href=True):

                absolute_url = urljoin(
                    response.url,
                    link["href"].strip()
                )

                parsed_url = urlparse(absolute_url)

                if parsed_url.scheme not in ("http", "https"):
                    continue

                link_host = (
                    parsed_url.hostname or ""
                ).lower().removeprefix("www.")

                if link_host != base_host:
                    continue

                if parsed_url.path.lower().endswith(
                    self.IGNORED_EXTENSIONS
                ):
                    continue

                clean_url = self._normalize_url(
                    absolute_url
                )

                if clean_url in seen_urls:
                    continue

                seen_urls.add(clean_url)

                if not robots.can_fetch(
                    self.USER_AGENT,
                    clean_url
                ):
                    skipped_by_robots += 1
                    continue

                anchor_text = link.get_text(
                    " ",
                    strip=True
                )

                discovered_links.append({
                    "url": clean_url,
                    "anchor_text": anchor_text
                })

                if len(discovered_links) >= self.MAX_DISCOVERED_LINKS:
                    break

            return {
                "status": "success",
                "total_links": len(discovered_links),
                "links": discovered_links,
                "skipped_by_robots": skipped_by_robots
            }

        except PermissionError as error:

            return {
                "status": "blocked_by_robots",
                "total_links": 0,
                "links": [],
                "error": str(error)
            }

        except requests.RequestException as error:

            return {
                "status": "failed",
                "total_links": 0,
                "links": [],
                "error": str(error)
            }
