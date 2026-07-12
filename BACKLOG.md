# BACKLOG — claude-red

## Next up (2026-07-12, priority order)
1. **Prove one non-Claude emitter end-to-end** — wire `dist/opencode/` or `agy` (conventions exist in `~/.agents`) into a real project via harness symlink; run a skill. Makes multi-agent real.
2. **Deepen the moat (first-activity content)** — RF/wireless + exploit-dev is where claude-sec (817) is empty. Execute roadmap splits (IoT/hardware, AD, web-advanced). Durable differentiator.
3. **Package as a Claude plugin** — copy claude-sec's `.claude-plugin/plugin.json` + `marketplace.json` so it's installable, not just clonable.
4. **Retire `convert_skills.py`** once an emitter covers Console ZIP export.

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
