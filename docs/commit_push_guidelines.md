# AutoWeave Library Commit And Push Guidelines

These rules apply while hardening the library runtime. The goal is to keep `main` moving in small, verifiable slices instead of batching large unreviewable changes.

## Working Model

Commit and push after each green vertical slice.

A valid slice should:

- change one coherent concern
- keep the library installable
- keep the relevant tests green
- be understandable from the commit message alone

Do not hold multiple unrelated runtime, packaging, and docs changes locally at the same time unless the changes are inseparable.

## Commit Scope

Prefer one of these scopes:

- `feat(runtime): ...`
- `feat(monitoring): ...`
- `feat(storage): ...`
- `feat(cli): ...`
- `fix(runtime): ...`
- `fix(queue): ...`
- `refactor(runtime): ...`
- `test(runtime): ...`
- `docs(runtime): ...`
- `chore(ci): ...`

Good commit examples:

- `feat(monitoring): add typed snapshot and action receipts`
- `fix(runtime): classify degraded snapshot failures explicitly`
- `chore(ci): add library wheel and pytest workflow`

Avoid:

- vague messages like `updates`, `changes`, or `fix stuff`
- mixing runtime logic, packaging, and unrelated docs in one commit
- committing generated junk or local state

## Required Verification Before Commit

Run the narrowest checks that prove the slice:

- focused tests for touched modules
- full `pytest` if the slice changes shared runtime behavior
- packaging smoke checks for package or CLI changes

Minimum expectation:

- no failing tests in touched areas
- no broken imports
- no partially edited public payload shape without updated tests

## Push Discipline

Push immediately after the slice is green.

Do not leave validated slices unpushed unless:

- the next change depends directly on unpushed code, and
- keeping it local materially reduces risk

If multiple slices are in flight, each slice should still have its own commit before moving on.

## Runtime Hardening Rules

For this library specifically:

- preserve current CLI and web-consumed monitoring contracts unless changes are additive
- treat OpenHands as the primary execution substrate for now
- prefer additive typed contracts over silent payload rewrites
- convert broad exception handling into explicit failure typing where practical
- keep refactors behavior-preserving unless the tests and docs are updated in the same slice

## What Not To Commit

Never commit:

- `.pytest_cache/`
- local virtualenv changes
- `var/` runtime state
- temporary workspaces
- ad hoc debug files
- secrets or copied credentials

## Recommended Loop

1. Pick one slice.
2. Implement only that slice.
3. Run focused checks, then broader checks if needed.
4. Commit with a scoped message.
5. Push `main`.
6. Start the next slice from a clean working tree.
