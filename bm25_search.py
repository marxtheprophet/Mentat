import json
from rank_bm25 import BM25Okapi


class BM25Search:
    def __init__(self, docs):
        self.documents = docs

        # tokenize documents
        self.corpus = [
            doc["content"].lower().split()
            for doc in docs
        ]

        # build BM25 index
        self.bm25 = BM25Okapi(self.corpus)

    def search(self, query, top_k=5):
        tokenized_query = query.lower().split()

        scores = self.bm25.get_scores(tokenized_query)

        # rank results
        ranked = sorted(
            zip(self.documents, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return ranked[:top_k]