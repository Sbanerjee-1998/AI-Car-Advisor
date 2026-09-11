from __future__ import annotations


def pack_context(messages: list[dict[str, str]], current_message: str, budget: int = 8000) -> list[dict[str, str]]:
    """Keep complete recent turns under a simple character/token approximation."""
    remaining = max(1000, budget * 4 - len(current_message))
    selected: list[dict[str, str]] = []
    for message in reversed(messages):
        size = len(message.get("content", ""))
        if size > remaining:
            break
        selected.insert(0, message)
        remaining -= size
    return selected
