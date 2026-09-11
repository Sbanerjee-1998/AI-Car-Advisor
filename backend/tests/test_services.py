from pathlib import Path

import pytest

from backend.app.agents.context import pack_context
from backend.app.services.catalog import CatalogService


def test_context_keeps_recent_complete_messages_within_budget():
    messages = [{"role": "user", "content": "old" * 1000}, {"role": "assistant", "content": "recent"}]
    selected = pack_context(messages, "current", budget=1)
    assert selected == [{"role": "assistant", "content": "recent"}]


def test_invalid_catalog_document_fails(tmp_path: Path):
    (tmp_path / "invalid.md").write_text("# no front matter", encoding="utf-8")
    with pytest.raises(ValueError, match="front matter"):
        CatalogService(tmp_path)
