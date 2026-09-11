from __future__ import annotations

import hashlib
import math


class DeterministicEmbeddings:
    """Small offline embedding adapter for tests and local fallback retrieval."""

    def __init__(self, dimensions: int = 64):
        self.dimensions = dimensions

    def embed_query(self, text: str) -> list[float]:
        values = [0.0] * self.dimensions
        for token in text.casefold().split():
            digest = hashlib.sha256(token.encode()).digest()
            index = int.from_bytes(digest[:2], "big") % self.dimensions
            values[index] += 1.0
        norm = math.sqrt(sum(value * value for value in values)) or 1.0
        return [value / norm for value in values]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_query(text) for text in texts]
