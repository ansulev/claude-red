# Deployment Targets

The skill **base** (`Skills/<category>/<skill>/SKILL.md`, YAML frontmatter + neutral
body) is the single source of truth. `tools/emit.py` renders it into per-agent trees
under `dist/<target>/` (gitignored). The base stays stable; only deployment varies.

```bash
python3 tools/emit.py --target all           # every implemented target
python3 tools/emit.py --target claude         # one target
```

## Symlink contract (harness)

`dist/` is disposable and regenerated. The harness symlinks the emitted tree an agent
needs into a project when that agent is engaged — the same pattern Claude `/engage`
uses to pull cybersec skills/prompts. Deploy paths per agent (Angel's `~/.agents` SoT +
per-project setup) reference `dist/<target>/`, never the base directly.

| Emitted layout | Symlink into |
|---|---|
| `dist/claude/<name>/SKILL.md` | `<project>/.claude/skills/` or `~/.claude/skills/` |
| `dist/codex/AGENTS.md` + `skills/` | `<project>/AGENTS.md` (+ `skills/`) |
| `dist/opencode/AGENTS.md` + `skills/` | `<project>/AGENTS.md` |
| `dist/generic/<name>.md` | anywhere; paste-ready |

## Implemented

| Target | Convention | Confidence |
|---|---|---|
| `claude` | Agent Skills — `<name>/SKILL.md`, YAML frontmatter, auto-discovered one level deep, trigger-loaded (no settings.json entry needed) | High |
| `codex` | `AGENTS.md` router + `skills/<name>.md` opened on demand | High |
| `opencode` | `AGENTS.md` (same as codex) | High |
| `generic` | per-skill markdown + `INDEX.md`, paste into any tool | High |

## Planned — convention needs verification before emitting

Add an `emit_<name>()` to `tools/emit.py` and register it in `TARGETS` once the
on-disk convention is confirmed. Do not fabricate a format.

| Target | Likely convention | Status |
|---|---|---|
| `grok` | grok-cli context/instructions file — verify | Convention TBD |
| `antigravity-cli` | Google Antigravity agent config — verify | Convention TBD |
| `kilocode` | `.kilocode/rules/` or custom modes — verify | Convention TBD |
| `pi` | verify | Convention TBD |
| `hermes` | Angel's framework (Node) — define | Owner-defined |
| `zeroclaw` / `ironclaw` / `picoclaw` | Angel's frameworks — define | Owner-defined |

## Claude skill load/unload (reference)

Personal Agent Skills are **filesystem-linked, trigger-loaded — not wired through
`settings.json`**. Load = drop `<name>/SKILL.md` into `~/.claude/skills/` (personal) or
`<project>/.claude/skills/` (project); Claude auto-discovers and loads on demand when the
conversation matches `description`. Unload = remove/move the folder. `settings.json` only
governs plugins/marketplaces and permissions, not individual personal skills.
