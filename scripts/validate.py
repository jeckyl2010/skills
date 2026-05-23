#!/usr/bin/env python3
"""
validate.py — validate all SKILL.md frontmatter against schemas/skill_schema.json

Usage:
    python3 scripts/validate.py           # validate all skills
    python3 scripts/validate.py --fix     # report fixable issues
"""

import json
import sys
import re
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("jsonschema not installed. Run: pip install jsonschema")
    sys.exit(1)

try:
    import yaml
except ImportError:
    print("pyyaml not installed. Run: pip install pyyaml")
    sys.exit(1)

ROOT = Path(__file__).parent.parent
SCHEMA_PATH = ROOT / "schemas" / "skill_schema.json"

def load_schema():
    return json.loads(SCHEMA_PATH.read_text())

def extract_frontmatter(path: Path):
    content = path.read_text()
    if not content.startswith("---"):
        return None, "No frontmatter found"
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, "Malformed frontmatter (no closing ---)"
    try:
        data = yaml.safe_load(parts[1])
        return data, None
    except yaml.YAMLError as e:
        return None, f"YAML parse error: {e}"

def validate_name_matches_dir(skill_path: Path, name: str):
    dir_name = skill_path.parent.name
    if name != dir_name:
        return f"name '{name}' does not match directory name '{dir_name}'"
    return None

def main():
    schema = load_schema()
    validator = jsonschema.Draft7Validator(schema)

    skills = sorted(ROOT.rglob("SKILL.md"))
    if not skills:
        print("No SKILL.md files found.")
        sys.exit(0)

    errors = []
    warnings = []

    for skill_path in skills:
        rel = skill_path.relative_to(ROOT)
        data, parse_error = extract_frontmatter(skill_path)

        if parse_error:
            errors.append(f"  {rel}: {parse_error}")
            continue

        for error in validator.iter_errors(data):
            errors.append(f"  {rel}: {error.message} (at {'.'.join(str(p) for p in error.path) or 'root'})")

        if data and "name" in data:
            name_error = validate_name_matches_dir(skill_path, data["name"])
            if name_error:
                errors.append(f"  {rel}: {name_error}")

        # Deprecation warnings — not errors, but visible
        if data and "deprecated_since" in data:
            superseded = data.get("superseded_by")
            msg = f"  {rel}: deprecated since {data['deprecated_since']}"
            if superseded:
                msg += f" — superseded by '{superseded}'"
            warnings.append(msg)

    total = len(skills)

    if warnings:
        print(f"Deprecation warnings — {len(warnings)} deprecated skill(s):\n")
        for w in warnings:
            print(w)
        print()

    if errors:
        print(f"Validation failed — {len(errors)} error(s) across {total} skill(s):\n")
        for e in errors:
            print(e)
        sys.exit(1)
    else:
        print(f"All {total} skill(s) valid.")

if __name__ == "__main__":
    main()
