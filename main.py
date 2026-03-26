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