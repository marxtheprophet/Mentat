import json
import re
from rank_bm25 import BM25Okapi
from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))


def tokenize(text):
    # lowercase
    text = text.lower()

    # remove punctuation
    text = re.sub(r'[^a-z0-9\s]', '', text)

    # split
    tokens = text.split()

    # remove stopwords
    tokens = [word for word in tokens if word not in stop_words]

    return tokens


class BM25Search:
    def __init__(self, docs):
        self.documents = docs

        self.corpus = [
            tokenize(doc["content"])
            for doc in docs
        ]

        self.bm25 = BM25Okapi(self.corpus)

    def search(self, query, top_k=5):
        tokenized_query = tokenize(query)

        scores = self.bm25.get_scores(tokenized_query)

        ranked = sorted(
            zip(self.documents, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return ranked[:top_k]