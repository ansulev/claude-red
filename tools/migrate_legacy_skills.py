#!/usr/bin/env python3
"""Migrate legacy '## Metadata' skills to the unified YAML-frontmatter base.

The repo had two skill formats. This normalizes every legacy skill (the ones
with a `## Metadata` / `## Full Methodology` layout) into the tool-neutral base
format already used by the rest of the library:

    ---
    name: <folder>
    description: "<one paragraph>"
    trigger_phrases:
      - "..."
    source: <url>
    ---

    <methodology body — no tool-specific scaffolding>

Idempotent: files already starting with `---` (YAML frontmatter) are skipped.
Run from the repo root: python3 tools/migrate_legacy_skills.py [--dry-run]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "Skills"


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def parse_legacy(text: str, folder_fallback: str) -> dict:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")

    name = None
    source = None
    description: list[str] = []
    triggers: list[str] = []
    body_start = None

    state = "INIT"
    for i, line in enumerate(lines):
        stripped = line.strip()
        header = re.match(r"^##\s+(.+)", stripped)
        if header:
            section = header.group(1).strip().lower()
            state = {
                "metadata": "META",
                "description": "DESC",
                "trigger phrases": "TRIG",
                "instructions for claude": "SKIP",
                "full methodology": "BODY",
            }.get(section, "SKIP")
            if state == "BODY":
                body_start = i + 1
                break
            continue

        if state == "META":
            m = re.match(r"-\s*\*\*([^*]+)\*\*\s*:\s*(.+)", stripped)
            if m:
                key, val = m.group(1).strip().lower(), m.group(2).strip()
                if key == "folder":
                    name = slugify(val)
                elif key == "source":
                    source = val
        elif state == "DESC" and stripped:
            description.append(stripped)
        elif state == "TRIG":
            m = re.search(r"`([^`]+)`", stripped)
            if m:
                triggers = [t.strip() for t in m.group(1).split(",") if t.strip()]

    body = "\n".join(lines[body_start:]).lstrip("\n") if body_start is not None else ""

    return {
        "name": name or slugify(folder_fallback),
        "description": " ".join(description).strip(),
        "triggers": triggers,
        "source": source,
        "body": body.rstrip() + "\n",
    }


def build(meta: dict) -> str:
    out = ["---", f"name: {meta['name']}"]
    out.append(f"description: {json.dumps(meta['description'], ensure_ascii=False)}")
    if meta["triggers"]:
        out.append("trigger_phrases:")
        out.extend(f"  - {json.dumps(t, ensure_ascii=False)}" for t in meta["triggers"])
    if meta["source"]:
        out.append(f"source: {meta['source']}")
    out.append("---\n")
    return "\n".join(out) + "\n" + meta["body"]


def main() -> int:
    dry = "--dry-run" in sys.argv
    if not SKILLS_DIR.is_dir():
        print(f"Error: {SKILLS_DIR} not found", file=sys.stderr)
        return 1

    migrated = skipped = 0
    for skill_md in sorted(SKILLS_DIR.rglob("SKILL.md")):
        text = skill_md.read_text(encoding="utf-8")
        if text.lstrip().startswith("---"):
            skipped += 1
            continue
        if "## Metadata" not in text or "## Full Methodology" not in text:
            print(f"!! SKIP (unexpected layout): {skill_md.relative_to(ROOT)}")
            skipped += 1
            continue
        meta = parse_legacy(text, skill_md.parent.name)
        if not meta["description"]:
            print(f"!! WARN empty description: {skill_md.relative_to(ROOT)}")
        new = build(meta)
        if dry:
            print(f"[dry-run] {skill_md.relative_to(ROOT)} -> name={meta['name']} "
                  f"triggers={len(meta['triggers'])} body={len(meta['body'])}B")
        else:
            skill_md.write_text(new, encoding="utf-8", newline="\n")
            print(f"OK {skill_md.relative_to(ROOT)}")
        migrated += 1

    print(f"\n{'Would migrate' if dry else 'Migrated'}: {migrated} | "
          f"skipped (already YAML): {skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
