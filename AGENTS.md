# AGENTS.md — claude-red
**v0.1 · 2026-07-12 · ANSULEV Group**
**Extends: ~/.claude/CLAUDE.md (global) + SYSTEM.md**
**Context source of truth — `CLAUDE.md` · `CODEX.md` · `GEMINI.md` · `OPENCODE.md` symlink here. Edit only this file.**

---

## PROJECT IDENTITY

- **Name**: claude-red
- **Vertical**: PROTISEC
- **Stack**: Python 3 skill tooling + markdown skill base (no runtime service)
- **Machine**: DEV
- **Repos**:
  - Gitea (private, pending): `git@gitea.nas:ansulev/claude-red.git`
  - GitHub: **not published** — private base, decoupled from upstream SnailSploit/claude-red

**GOAL**
A tool-neutral offensive-security skill base with per-agent emitters — author once, deploy the same skills into any coding agent (Claude, Codex, opencode, Gemini/agy, …) via symlink-on-demand.

> **Authorized use only.** Offensive/dual-use content. Use for sanctioned red team, bug bounty, research, CTF.

---

## AGENT ROUTING

- **Claude** `claude` — default for real work: base normalization, emitter design, security judgment.
- **Gemini** `antigravity-cli` (agy) — trivial/non-sensitive bulk only. Never client/engagement data.
- **opencode** — emitter target; AGENTS.md-native.
- **codex** — emitter target; AGENTS.md-native.
- **Rule:** engagement/PII/client data → Claude or LOCAL only; never cloud Gemini/codex.

---

## ARCHITECTURE

```
Skills/<category>/<skill>/SKILL.md   base (SoT): YAML frontmatter + neutral body
        │
        ├─ tools/migrate_legacy_skills.py   legacy ## Metadata → base (idempotent)
        ├─ tools/build_manifest.py          → claude-skills.json (single indexer)
        └─ tools/emit.py --target <agent>   → dist/<target>/  (gitignored)
                                              claude · codex · opencode · generic
                                              → harness symlinks dist/<target>/ into a project on engage
```

**Key dependencies**: none external. Pure-stdlib Python. `emit.py` reuses `build_manifest.parse_frontmatter`.

---

## ACTIVE SPRINT

<!-- Full backlog → BACKLOG.md -->
- [ ] Add emitter targets (grok/antigravity-cli/kilocode/pi/hermes/*claws) — convention-first, no fabrication
- [ ] Push to Gitea private once operative; update README_GIT.md remotes
- [ ] Wire `~/.agents` SoT → per-project symlink of `dist/<target>/`

---

## PROJECT-SPECIFIC RULES

### Entry point
```bash
python3 tools/emit.py --target all       # render base → dist/<target>/
```

### Verification
```bash
python3 tools/build_manifest.py && python3 tools/emit.py --target all
# expect: 0 empty descriptions, no placeholder leaks
```

### Key files & directories
| Path | Purpose | Do Not Touch? |
|------|---------|---------------|
| `Skills/` | skill base (SoT) — edit skills here | |
| `tools/migrate_legacy_skills.py` | legacy→base normalizer | |
| `tools/emit.py` + `TARGETS.md` | multi-agent emitter | |
| `tools/build_manifest.py` | single manifest indexer | |
| `dist/` | generated per-agent output | ✓ (regenerated) |
| `convert_skills.py` | deprecated legacy ZIP path | ✓ (pending removal) |

### Constraints
- Skill bodies stay **tool-neutral** — no "for Claude" scaffolding; agent specifics live in emitters only.
- After any upstream pull: `migrate_legacy_skills.py` → `build_manifest.py` → `emit.py` (README_GIT.md).
- Root `AGENTS.md` (this file) = how to work ON the repo; `dist/codex/AGENTS.md` = emitted skill router. Distinct.

---

## DO NOT TOUCH (without explicit instruction)
- Skill frontmatter format — regenerate via `migrate_legacy_skills.py`, never hand-edit for merges.
- Version strings (`claude-skills.json` version, README badge) — Angel owns versioning.

---

## DEFINITION OF DONE
1. ✓ `ruff check .` clean on touched Python
2. ✓ Verification command exits 0 (0 empty descriptions, no leaks)
3. ✓ Commit convention: `type(scope): description`
4. ✓ Docs updated (README_GIT / TARGETS / BACKLOG) if workflow changed

---

## USEFUL LINKS
- Global `~/.claude/CLAUDE.md` · `SYSTEM.md` · `~/.claude/rules/`
- Project: `README_GIT.md` (sync workflow) · `TARGETS.md` (emitter targets) · `BACKLOG.md`
