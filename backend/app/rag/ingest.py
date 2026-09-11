from __future__ import annotations

import argparse
from pathlib import Path

from backend.app.services.catalog import CatalogService


def ingest(source: str, _chroma_path: str) -> int:
    catalog = CatalogService(Path(source))
    return len(catalog.vehicles)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="backend/data/cars")
    parser.add_argument("--chroma-path", default=".local/chroma")
    args = parser.parse_args()
    print(f"Validated {ingest(args.source, args.chroma_path)} curated vehicle documents")
