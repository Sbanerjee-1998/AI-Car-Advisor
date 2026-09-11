from __future__ import annotations

from backend.app.services.catalog import CatalogService, Vehicle


class CatalogRetriever:
    def __init__(self, catalog: CatalogService):
        self.catalog = catalog

    def retrieve(self, query: str, filters: dict | None = None, limit: int = 3) -> list[Vehicle]:
        return self.catalog.search(query, filters, min(limit, 3))
