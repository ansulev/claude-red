# Git Workflow — claude-red (private base)

This fork is a **decoupled private base**, not an upstream dependency. Upstream is a
read-only *content* feed: pull new skill methodology, then re-normalize it through our
tooling. The base format (unified YAML frontmatter + neutral body) and the emitter are
ours and stay stable. See `TARGETS.md` and the project memory.

## Remotes

| Remote   | URL                                 | Purpose               |
|----------|-------------------------------------|-----------------------|
| origin   | github.com/ansulev/claude-red       | This fork — push here |
| upstream | github.com/SnailSploit/claude-red   | Source — pull only    |

## Sync upstream → this fork (pull, merge, re-normalize)

```bash
git fetch upstream
git merge upstream/main                     # conflicts EXPECTED in Skills/ we normalized

# Resolve conflicts by taking upstream CONTENT, then re-normalize (all idempotent):
python3 tools/migrate_legacy_skills.py      # any legacy ## Metadata skill → unified YAML base
python3 tools/build_manifest.py             # regenerate claude-skills.json (single indexer)
python3 tools/emit.py --target all          # regenerate dist/ per-agent trees (gitignored)

git push origin main
```

`migrate_legacy_skills.py` skips files already in YAML frontmatter, so re-running it only
touches upstream skills still in the old format. `dist/`, `skills-converted/`, `skills-zip/`
are generated and gitignored — never merge-relevant.

## Conflict expectation

Upstream still ships two formats and edits `Skills/` freely, so **merges will conflict on
any skill we normalized**. Resolution rule: keep upstream's *methodology content*, discard
its format scaffolding (`## Metadata` / `## Instructions for Claude` / `## Full
Methodology`), then let `migrate_legacy_skills.py` re-impose the base format. Never hand-fix
frontmatter — regenerate.

## This fork's divergence vs upstream

| Area | Change |
|------|--------|
| Skill format | Unified all 58 skills to one YAML-frontmatter base (was 26 YAML / 32 legacy) |
| `tools/migrate_legacy_skills.py` | New — legacy → base normalizer (idempotent) |
| `tools/emit.py` + `TARGETS.md` | New — multi-agent emitter (claude/codex/opencode/generic; more planned) |
| `tools/build_manifest.py` | Single manifest indexer; `claude-skills.json` now complete |
| `convert_skills.py` | Deprecated (legacy Claude-Console ZIP path); pending removal |
| Deletions | `.github/workflows/python-publish.yml` (dead PyPI job), tracked `.DS_Store` |
| `.gitignore` | New — excludes generated `dist/`, `skills-converted/`, `skills-zip/`, caches |

None submitted upstream — upstream management is stalled/inconsistent; this base is
maintained independently.
