#!/usr/bin/env python3
"""
index_builder.py — generate index.yaml from all SKILL.md files

Usage:
    python3 scripts/index_builder.py

Writes index.yaml to the repo root. Safe to re-run at any time.
"""

import sys
from pathlib import Path
from datetime import date

try:
    import yaml
except ImportError:
    print("pyyaml not installed. Run: pip install pyyaml")
    sys.exit(1)

ROOT = Path(__file__).parent.parent

def extract_frontmatter(path: Path):
    content = path.read_text()
    if not content.startswith("---"):
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        return yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None

def main():
    skills = sorted(ROOT.rglob("SKILL.md"))
    index = {"generated": str(date.today()), "skills": []}

    for skill_path in skills:
        data = extract_frontmatter(skill_path)
        if not data:
            print(f"Skipping {skill_path.relative_to(ROOT)} — no valid frontmatter")
            continue

        rel_dir = skill_path.parent.relative_to(ROOT)
        parts = rel_dir.parts  # e.g. ('engineering', 'senior-software-architecture')
        category = parts[0] if len(parts) >= 2 else "uncategorized"

        entry = {
            "name": data.get("name", skill_path.parent.name),
            "category": category,
            "path": str(rel_dir),
            "description": data.get("description", ""),
            "version": data.get("version", ""),
            "tags": data.get("tags", []),
            "tool_agnostic": data.get("tool_agnostic", None),
            "tested_on": data.get("tested_on", None),
            "deprecated_since": data.get("deprecated_since", None),
            "superseded_by": data.get("superseded_by", None),
        }
        # Clean up None/empty values
        entry = {k: v for k, v in entry.items() if v is not None and v != []}
        index["skills"].append(entry)

    out = ROOT / "index.yaml"
    with open(out, "w") as f:
        yaml.dump(index, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"index.yaml written — {len(index['skills'])} skill(s) indexed.")

if __name__ == "__main__":
    main()
