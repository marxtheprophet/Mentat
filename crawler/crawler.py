import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import hashlib


class Crawler:
    def __init__(self, seeds, max_pages=200, max_depth=2):
        self.queue = [(url, 0) for url in seeds]
        self.visited = set()
        self.seen_hashes = set()
        self.documents = []

        self.max_pages = max_pages
        self.max_depth = max_depth

        self.allowed_domains = ["reddit.com", "medium.com", "github.com"]

    def is_allowed(self, url):
        domain = urlparse(url).netloc
        return any(d in domain for d in self.allowed_domains)

    def fetch(self, url):
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=5)
            return response.text
        except:
            return None

    def parse(self, html, base_url):
        soup = BeautifulSoup(html, "html.parser")

        title = soup.title.string if soup.title else ""

        paragraphs = soup.find_all("p")
        content = " ".join([p.get_text() for p in paragraphs])

        links = []

        for a in soup.find_all("a", href=True):
            link = urljoin(base_url, a["href"])

            if not self.is_allowed(link):
                continue

            # skip junk/system links
            if any(x in link for x in ["login", "signup", "api", "#", "help", "about"]):
                continue

            # Reddit → only post pages
            if "reddit.com" in link:
                if "/comments/" not in link:
                    continue

            # Medium → skip tag pages
            if "medium.com" in link:
                if "/tag/" in link:
                    continue

            # GitHub → STRICT: only github.com/user/repo
            if "github.com" in link:
                parts = link.split("/")

                # must be exactly: github.com/user/repo
                if len(parts) != 5:
                    continue

                # block non-user namespaces
                if parts[3] in [
                    "features", "topics", "collections", "about",
                    "resources", "docs", "orgs", "sponsors",
                    "search", "security", "enterprise", "solutions"
                ]:
                    continue

            links.append(link)

        return title, content, links

    def is_duplicate(self, text):
        h = hashlib.sha256(text.encode()).hexdigest()
        if h in self.seen_hashes:
            return True
        self.seen_hashes.add(h)
        return False

    def crawl(self):
        while self.queue and len(self.documents) < self.max_pages:
            url, depth = self.queue.pop(0)

            if url in self.visited or depth > self.max_depth:
                continue

            print("Crawling:", url)
            self.visited.add(url)

            html = self.fetch(url)
            if not html:
                continue

            title, content, links = self.parse(html, url)

            if not content.strip() or self.is_duplicate(content):
                continue

            self.documents.append({
                "url": url,
                "title": title,
                "content": content[:5000]
            })

            if len(self.documents) >= self.max_pages:
                break

            for link in links:
                if link not in self.visited:
                    self.queue.append((link, depth + 1))

            time.sleep(1)

        return self.documents