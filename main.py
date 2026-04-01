# from crawler.crawler import Crawler
# import json

# SEEDS = [
#     "https://old.reddit.com/r/programming/",
#     "https://medium.com/tag/programming",
#     "https://github.com/topics/programming"
# ]

# crawler = Crawler(SEEDS, max_pages=200, max_depth=2)
# docs = crawler.crawl()

# with open("data/documents.json", "w") as f:
#     json.dump(docs, f, indent=2)

# print(f"Collected {len(docs)} documents")

# import json
# from crawler.crawler import Crawler

# github_seeds = [
#     "https://github.com/topics/programming",
#     "https://github.com/topics/react"
# ]

# reddit_seeds = [
#     "https://old.reddit.com/r/programming/",
#     "https://old.reddit.com/r/webdev/"
# ]

# medium_seeds = [
#     "https://medium.com/tag/programming",
#     "https://medium.com/tag/web-development"
# ]

# crawler_github = Crawler(github_seeds, max_pages=300)
# crawler_reddit = Crawler(reddit_seeds, max_pages=400)
# crawler_medium = Crawler(medium_seeds, max_pages=300)

# docs_github = crawler_github.crawl()
# docs_reddit = crawler_reddit.crawl()
# docs_medium = crawler_medium.crawl()

# all_docs = docs_github + docs_reddit + docs_medium

# with open("data/documents.json", "w") as f:
#     json.dump(all_docs, f, indent=2)

# print("Total documents:", len(all_docs))


import json

from bm25_search import BM25Search

# load documents
with open("data/documents.json") as f:
    docs = json.load(f)

search_engine = BM25Search(docs)

query = input("Search: ")

results = search_engine.search(query)

for doc, score in results:
    print("\n---")
    print("Score:", score)
    print("Title:", doc["title"])
    print("URL:", doc["url"])
