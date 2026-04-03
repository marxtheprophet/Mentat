import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import hashlib


class Crawler:
    def __init__(self, seeds, max_pages=5000, max_depth=2):
        self.queue = [(url, 0) for url in seeds]
        self.visited = set()
        self.seen_hashes = set()
        self.documents = []

        self.max_pages = max_pages
        self.max_depth = max_depth

    def is_allowed(self, url):
        return any(d in url for d in ["github.com", "reddit.com", "medium.com"])

    def get_delay(self, url):
        if "github.com" in url:
            return 0.5
        if "reddit.com" in url:
            return 1.5
        if "medium.com" in url:
            return 1.5
        return 1

    def fetch(self, url):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                "Accept-Language": "en-US,en;q=0.9"
            }
            response = requests.get(url, headers=headers, timeout=5)
            return response.text
        except:
            return None

    def is_blocked(self, html):
        if not html:
            return True
        html = html.lower()
        return any(x in html for x in [
            "access denied", "blocked", "rate limit", "captcha"
        ])

    def parse(self, html, base_url):
        soup = BeautifulSoup(html, "html.parser")

        # safe title extraction
        title = soup.title.string.strip() if soup.title and soup.title.string else ""

        # extract content
        paragraphs = soup.find_all("p")
        content = " ".join([p.get_text().strip() for p in paragraphs])

        links = []

        for a in soup.find_all("a", href=True):
            link = urljoin(base_url, a["href"])

            # only allowed domains
            if not self.is_allowed(link):
                continue

            # skip useless pages
            if any(x in link for x in ["login", "signup", "api", "#", "help", "about"]):
                continue

            # Reddit → only post pages
            if "reddit.com" in link:
                if "/comments/" not in link:
                    continue

            # Medium → only article pages
            if "medium.com" in link:
                if "/@" not in link:
                    continue

            # GitHub → only repo root
            if "github.com" in link:
                parts = link.split("/")
                if len(parts) != 5:
                    continue

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

            # skip visited or too deep
            if url in self.visited or depth > self.max_depth:
                continue

            # force old reddit only
            if "reddit.com" in url and "old.reddit.com" not in url:
                continue

            print("Crawling:", url)
            self.visited.add(url)

            html = self.fetch(url)

            # skip blocked or failed pages
            if not html or self.is_blocked(html):
                continue

            title, content, links = self.parse(html, url)

            # skip low-quality pages
            if not content or len(content.split()) < 50:
                continue

            # deduplication
            if self.is_duplicate(content):
                continue

            # create preview snippet
            preview = content[:200]

            # store document
            self.documents.append({
                "url": url,
                "title": title,
                "content": content[:5000],
                "preview": preview
            })

            print("Docs collected:", len(self.documents))

            if len(self.documents) >= self.max_pages:
                break

            # add new links to queue (with control)
            for link in links:
                if link not in self.visited and len(self.queue) < 10000:
                    self.queue.append((link, depth + 1))

            # respect rate limits
            time.sleep(self.get_delay(url))

        return self.documents