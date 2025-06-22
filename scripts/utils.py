import time
import random
import re
import html
import json
from pathlib import Path
from typing import Any


def human_delay(min_sec: float = 1.0, max_sec: float = 4.0) -> None:
    """Pause randomly to mimic human browsing."""
    time.sleep(random.uniform(min_sec, max_sec))


def clean_text_for_llm(raw: str) -> str:
    """Strip non-ASCII, collapse blank lines, normalize bullets."""
    text = html.unescape(raw)
    text = re.sub(r"[^\x00-\x7F]+", "", text)
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[\-\•\-\—·]", "-", text)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def load_json(file_path: Path) -> Any:
    """Load and return JSON from disk."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: Any, file_path: Path) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


