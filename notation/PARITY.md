# Notation Parity With Exploration Specs

This document tracks which exploration-contract capabilities already have a notation-language representation and which ones still require raw JSON.

## Covered By Notation

- `seed`
- `hidden_ranges` for one or both players
  - exact hands
  - ordered hands
  - weighted branches
  - rank-class, rank-set, suit-set, and conjunctive card predicates
- `hidden_plays` for the current round
  - exact cards
  - weighted alternatives
  - conjunctive card predicates
- `completed_hidden_plays`
  - exact cards
  - weighted alternatives
  - multiple distinct `(round_index, player)` targets in one script
- `pending_hand.turnup`
  - exact turnup only, through `deal(turnup=...)`
- multi-statement scripts that combine:
  - `seed`
  - `deal(...)`
  - player hand ranges
  - current hidden plays
  - completed hidden plays

## Covered In Workflow Fixtures

The notation corpus now includes workflow-shaped fixtures for:

- pre-deal exact turnup plus weighted villain hand setup
- pre-deal scripts that specify one full player hand before the deal
- both-player hidden-range scripts in an active hand
- same-player scripts that combine a completed hidden-play range with a remaining-hand range
- commented multi-line scripts used like lab snippets

## Still Raw JSON Only

These exploration features still rely on raw JSON today:

- `base_state`
  - notation compiles only a fragment, not a full anchored exploration request
- engine-validation and resolver expectations
  - notation fixtures stop at parser output
- direct expression of exploration-only error cases like:
  - no active hand
  - no completed hidden play to override
  - duplicate-card collision in resolved states
  - no candidate hands after sampling constraints
- turnup uncertainty
  - notation currently supports only exact `turnup=...`

## Intentional Boundary

This is a good split.

Notation should remain a concise authoring layer for the useful fragment of the exploration contract. The exact `base_state`, resolution semantics, and engine-validity constraints should continue living in the transport-neutral exploration JSON contract and its executable fixture corpus.

## Planning Implication

At the moment, there is no urgent parity gap blocking product progress.

That means future notation work should mostly be triggered by:

- a specific lab workflow that still requires raw JSON too often
- a missing exploration feature that becomes product-relevant
- parser portability or conformance needs

Until one of those happens, the healthier project move is to keep product-flow work in front.
