# Exploration Specs

This directory defines the partial-state exploration layer that sits on top of the exact Truco engine.

Use these specs when the goal is not "run this exact state" but rather "start from this exact public state plus these weighted hidden-information assumptions, then resolve a concrete playable state."

That includes both:

- active-hand hidden ranges
- active-hand hidden face-down play identity, including completed rounds
- pre-deal nature-node specs that materialize a fresh hand from an idle match state

Files:

- `CONTRACT.md`: transport-neutral exploration contract
- `ASPECTS.md`: coverage map for exploration behavior
- `WORKFLOW.md`: authoring order for expanding the exploration language
- `aspects/`: per-aspect scenario planning docs
- `schemas/`: JSON schemas for exploration fixtures
- `fixtures/`: executable exploration fixtures

The engine remains exact. Exploration specs resolve to an exact `MatchState`, and only then does normal game execution continue.
`schemas/fixture.schema.json` references the normative engine
`match-state.schema.json` for every `base_state`; expected resolved states are
documented recursive subset assertions.

The separate [`notation/`](../notation/) surface is the normative authoring
language that compiles into this JSON contract.

## Current Recommendation

The exploration layer is already strong enough for current product work, engine debugging, and future analysis tooling.

That means the main near-term emphasis should usually be:

- adding exploration coverage only when a concrete product or analysis workflow needs it
- keeping the executable exploration corpus healthy
- spending most implementation energy on the playable app and product flow

In other words: exploration is no longer the main blocker for the project's next milestone.
