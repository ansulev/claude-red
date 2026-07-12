# BACKLOG — claude-red

## Emitter targets

The base (`Skills/`) + `tools/emit.py` render per-agent trees into `dist/<target>/`.
Add a target by writing `emit_<name>(skills, out)` in `tools/emit.py`, registering it
in `TARGETS`, and documenting its convention in `TARGETS.md`. **Do not fabricate a
format — confirm the agent's on-disk convention first.**

### Implemented
- [x] claude — Agent Skills `<name>/SKILL.md`
- [x] codex — `AGENTS.md` router + `skills/*.md`
- [x] opencode — `AGENTS.md` (shares codex emitter)
- [x] generic — per-skill markdown + `INDEX.md`

### To build (owner prep required first)
- [ ] antigravity-cli (`agy`) — model from Angel's existing agy setup in `~/.agents`
- [ ] opencode — refine against Angel's existing opencode setup if it diverges from AGENTS.md
- [ ] grok — **from zero**; confirm grok-cli on-disk convention before emitting
- [ ] kilocode — confirm `.kilocode/rules/` or custom-modes convention
- [ ] pi — confirm convention
- [ ] hermes — Angel's framework (Node); owner-defined layout
- [ ] zeroclaw / ironclaw / picoclaw — Angel's frameworks; owner-defined layout

## Deployment / harness
- [ ] Wire `~/.agents` SoT → per-project symlink of `dist/<target>/` (the `/engage` pattern)
- [ ] Repoint `install.sh` at `dist/claude/` (flat, discovers correctly) instead of nested `Skills/`

## Repo hygiene
- [ ] Push to **Gitea (private)** once operative — not GitHub. Update `README_GIT.md` remotes.
- [ ] Remove deprecated `convert_skills.py` once the emitter covers Claude-Console ZIP export
- [ ] Version policy: single source (manifest hardcodes 0.2.0; README badge says 58) — owner decides

## Content
- [ ] Split monolithic skills (`crash-analysis`, `windows-*` are 400–550 KB) into focused surfaces
