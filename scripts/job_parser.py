from pathlib import Path
import json
from typing import List, Dict
from scripts.config import OUTPUT_FILE, MARKDOWN_FILE


def save_results_json(data: List[Dict], path: Path = OUTPUT_FILE):
    """Write analysis data to JSON file."""
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def save_results_markdown(data: List[Dict], path: Path = MARKDOWN_FILE):
    """Write analysis data to a Markdown report."""
    path.parent.mkdir(exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write("# Job Analysis Results\n\n")
        for job in data:
            f.write(f"## {job['Company']} - {job['Job Role']}\n")
            f.write(f"- **Location**: {job['Location']}\n")
            f.write(f"- **Link**: {job.get('Job Link','N/A')}\n\n")
            f.write(job["analysis"] + "\n\n---\n\n")