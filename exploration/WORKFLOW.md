# Exploration Workflow

Use this workflow when expanding the exploration language.

## Authoring Order

1. update `ASPECTS.md` if a new coverage area is being introduced
2. expand or add an aspect doc under `aspects/`
3. if the contract changes, update `CONTRACT.md`
4. if executable coverage is possible now, add or update fixture files under `fixtures/`
5. if the fixture format changes, update `schemas/`
6. run both:
   - Rust in-process exploration fixture execution
   - Python schema/integrity validation

## Fixture Writing Rules

- each fixture should focus on one semantic question
- prefer exact expected states for deterministic branches
- use seeded sampling whenever more than one candidate could match
- use `expect_error` for rejected specs
- keep `base_state` exact and valid unless the fixture is explicitly about invalid base-state rejection

## Directory Ownership

- `aspects/` is the planning surface
- `fixtures/` is the executable corpus
- `schemas/` is the machine-checkable contract surface

## Current Recommendation

Before adding pretty user-facing notation, prefer growing the JSON contract and fixture corpus first.

That keeps the semantics stable while syntax is still evolving.
