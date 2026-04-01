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
from crawler.crawler import Crawler

github_seeds = [
    "https://github.com/topics/react",
    "https://github.com/topics/javascript",
    "https://github.com/topics/typescript",
    "https://github.com/topics/nodejs",
    "https://github.com/topics/python",
    "https://github.com/topics/backend",
    "https://github.com/topics/frontend",
    "https://github.com/topics/fullstack",
    "https://github.com/topics/api",
    "https://github.com/topics/database",
    "https://github.com/topics/mongodb",
    "https://github.com/topics/sql",
    "https://github.com/topics/system-design",
    "https://github.com/topics/microservices",
    "https://github.com/topics/docker",
    "https://github.com/topics/kubernetes",
    "https://github.com/topics/devops",
    "https://github.com/topics/machine-learning",
    "https://github.com/topics/data-science",
    "https://github.com/topics/algorithms"
]

reddit_seeds = [
    "https://old.reddit.com/r/programming/",
    "https://old.reddit.com/r/webdev/",
    "https://old.reddit.com/r/reactjs/",
    "https://old.reddit.com/r/javascript/",
    "https://old.reddit.com/r/node/",
    "https://old.reddit.com/r/python/",
    "https://old.reddit.com/r/learnprogramming/",
    "https://old.reddit.com/r/devops/",
    "https://old.reddit.com/r/docker/",
    "https://old.reddit.com/r/kubernetes/",
    "https://old.reddit.com/r/machinelearning/",
    "https://old.reddit.com/r/datascience/"
]

medium_seeds = [
    "https://medium.com/tag/programming",
    "https://medium.com/tag/software-engineering",
    "https://medium.com/tag/web-development",
    "https://medium.com/tag/javascript",
    "https://medium.com/tag/python",
    "https://medium.com/tag/nodejs",
    "https://medium.com/tag/react",
    "https://medium.com/tag/devops",
    "https://medium.com/tag/docker",
    "https://medium.com/tag/kubernetes",
    "https://medium.com/tag/system-design",
    "https://medium.com/tag/machine-learning",
    "https://medium.com/tag/data-science"
]

crawler_github = Crawler(github_seeds, max_pages=5000)
crawler_reddit = Crawler(reddit_seeds, max_pages=5000)
crawler_medium = Crawler(medium_seeds, max_pages=5000)

docs_github = crawler_github.crawl()
docs_reddit = crawler_reddit.crawl()
docs_medium = crawler_medium.crawl()

all_docs = docs_github + docs_reddit + docs_medium

with open("data/documents.json", "w") as f:
    json.dump(all_docs, f)

print("Total documents:", len(all_docs))


#search

# import json
# from bm25_search import BM25Search

# with open("data/documents.json") as f:
#     docs = json.load(f)

# search_engine = BM25Search(docs)

# query = input("Search: ")

# results = search_engine.search(query)

# for doc, score in results:
#     print("\n---")
#     print("Score:", score)
#     print("Title:", doc["title"])
#     print("URL:", doc["url"])
