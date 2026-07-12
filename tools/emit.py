#!/usr/bin/env python3
"""Emit the tool-neutral skill base into per-agent deployment trees.

Base (SoT) = Skills/<category>/<skill>/SKILL.md (YAML frontmatter + neutral body).
Each emitter renders that base into one coding agent's on-disk convention under
dist/<target>/. The harness symlinks the relevant dist/<target>/ into a project
when that agent is engaged (base stays put; deployment varies per agent).

Usage:
    python3 tools/emit.py --target claude|codex|opencode|generic|all [--out dist]

Adding a target: write an emit_<name>(skills, out) that writes dist/<name>/,
register it in TARGETS, document its convention + confidence in TARGETS.md.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from build_manifest import parse_frontmatter  # reuse the proven frontmatter reader

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "Skills"

FRONTMATTER_STRIP = re.compile(r"^---\n.*?\n---\n?", re.DOTALL)
TRIGGER_BLOCK = re.compile(r"^trigger_phrases:\n((?:[ \t]+-[ \t]*.+\n?)+)", re.M)


def load_skills() -> list[dict]:
    skills: list[dict] = []
    for skill_md in sorted(SKILLS_DIR.rglob("SKILL.md")):
        text = skill_md.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        body = FRONTMATTER_STRIP.sub("", text, count=1).lstrip("\n").rstrip() + "\n"
        triggers: list[str] = []
        m = TRIGGER_BLOCK.search(text)
        if m:
            triggers = [
                re.sub(r"^[ \t]*-[ \t]*", "", ln).strip().strip('"')
                for ln in m.group(1).splitlines()
                if ln.strip()
            ]
        skills.append(
            {
                "name": fm.get("name", skill_md.parent.name),
                "description": fm.get("description", ""),
                "triggers": triggers,
                "source": fm.get("source", ""),
                "category": skill_md.relative_to(SKILLS_DIR).parts[0],
                "body": body,
            }
        )
    return skills


def _frontmatter(s: dict) -> str:
    out = ["---", f"name: {s['name']}", f"description: {json.dumps(s['description'], ensure_ascii=False)}"]
    if s["triggers"]:
        out.append("trigger_phrases:")
        out += [f"  - {json.dumps(t, ensure_ascii=False)}" for t in s["triggers"]]
    if s["source"]:
        out.append(f"source: {s['source']}")
    out.append("---\n")
    return "\n".join(out)


def emit_claude(skills: list[dict], out: Path) -> int:
    """Claude Agent Skills: dist/claude/<name>/SKILL.md (flat, one level deep)."""
    base = out / "claude"
    for s in skills:
        d = base / s["name"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "SKILL.md").write_text(_frontmatter(s) + "\n" + s["body"], encoding="utf-8", newline="\n")
    return len(skills)


def _emit_agents_md(skills: list[dict], out: Path, target: str) -> int:
    """AGENTS.md router + per-skill files (codex, opencode, and AGENTS.md-aware tools)."""
    base = out / target
    sk = base / "skills"
    sk.mkdir(parents=True, exist_ok=True)
    for s in skills:
        (sk / f"{s['name']}.md").write_text(
            f"# {s['name']}\n\n{s['description']}\n\n---\n\n{s['body']}",
            encoding="utf-8",
            newline="\n",
        )
    lines = [
        "# Offensive Security Skills (claude-red base)",
        "",
        "Load the matching skill file from `skills/` when the task hits its triggers.",
        "Each file is a self-contained methodology; open it on demand, don't preload all.",
        "",
    ]
    for cat in sorted({s["category"] for s in skills}):
        lines.append(f"## {cat}")
        for s in sorted((x for x in skills if x["category"] == cat), key=lambda x: x["name"]):
            trig = f" — triggers: {', '.join(s['triggers'][:6])}" if s["triggers"] else ""
            lines.append(f"- `skills/{s['name']}.md` — {s['description'][:140]}{trig}")
        lines.append("")
    (base / "AGENTS.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    return len(skills)


def emit_codex(skills: list[dict], out: Path) -> int:
    return _emit_agents_md(skills, out, "codex")


def emit_opencode(skills: list[dict], out: Path) -> int:
    return _emit_agents_md(skills, out, "opencode")


def emit_generic(skills: list[dict], out: Path) -> int:
    """Lowest common denominator: dist/generic/<name>.md + INDEX.md any tool can paste."""
    base = out / "generic"
    base.mkdir(parents=True, exist_ok=True)
    for s in skills:
        (base / f"{s['name']}.md").write_text(_frontmatter(s) + "\n" + s["body"], encoding="utf-8", newline="\n")
    index = ["# claude-red — skill index", ""]
    for cat in sorted({s["category"] for s in skills}):
        index.append(f"## {cat}")
        for s in sorted((x for x in skills if x["category"] == cat), key=lambda x: x["name"]):
            index.append(f"- [{s['name']}]({s['name']}.md) — {s['description'][:140]}")
        index.append("")
    (base / "INDEX.md").write_text("\n".join(index), encoding="utf-8", newline="\n")
    return len(skills)


TARGETS = {
    "claude": emit_claude,
    "codex": emit_codex,
    "opencode": emit_opencode,
    "generic": emit_generic,
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--target", required=True, choices=[*TARGETS, "all"])
    ap.add_argument("--out", default="dist", help="output root (default: dist)")
    args = ap.parse_args()

    if not SKILLS_DIR.is_dir():
        print(f"Error: {SKILLS_DIR} not found")
        return 1

    skills = load_skills()
    out = (ROOT / args.out).resolve()
    targets = list(TARGETS) if args.target == "all" else [args.target]
    for t in targets:
        n = TARGETS[t](skills, out)
        print(f"emitted {n} skills -> {out.relative_to(ROOT)}/{t}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
