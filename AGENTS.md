# Agent Instructions

Whenever possible, follow test-driven development (TDD); prefer TDD whenever practical.

This is a small educational project created for a YouTube video and learning.
Prefer focused fixes to existing behavior; avoid expanding features or promising
broad platform support without explicit maintainer approval.

## Git worktrees

All new Git worktrees must live under
`~/sannux-data/worktrees/<repo>/<worktree_name>`. Never create them inside a
project checkout or as its sibling. This host-local root is excluded from
`synchosts`; transfer anything needed on another host deliberately. Do not move
or remove existing worktrees solely to satisfy this policy.

## Agent skills

### Issue tracker

Use GitHub Issues and external pull requests through `gh`. See `docs/agents/issue-tracker.md`.

### Triage labels

Use the canonical category and state labels. See `docs/agents/triage-labels.md`.

### Domain docs

Use a single repository-wide context, created only when needed. See `docs/agents/domain.md`.
