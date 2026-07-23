# Exploration Contract

## Purpose

This document defines a partial-state exploration layer that sits on top of the exact engine.

The engine remains deterministic and exact. Exploration specs describe hidden-information uncertainty and weighted ranges, then resolve to a concrete `MatchState` that the engine can run normally.

## Design Principles

- Keep the engine exact.
- Represent uncertainty outside the engine core.
- Allow both feasibility-style ranges and weighted posterior-style ranges.
- Make all sampling reproducible when a seed is provided.
- Treat the exploration language as a transport-neutral contract, not a UI-only notation.

## Core Idea

An exploration request starts from an exact `MatchState` and replaces some hidden information with a weighted range specification.

The current executable subset focuses on hidden remaining hands during an active hand.

## Top-Level Shape

```json
{
  "base_state": { "... exact MatchState ..." },
  "pending_hand": {
    "turnup": { "rank": "A", "suit": "SPADES" }
  },
  "hidden_plays": {
    "0": {
      "weighted_cards": [
        {
          "weight": 1,
          "card": { "exact": { "rank": "A", "suit": "HEARTS" } }
        }
      ]
    }
  },
  "completed_hidden_plays": [
    {
      "round_index": 0,
      "player": 0,
      "weighted_cards": [
        {
          "weight": 1,
          "card": { "exact": { "rank": "A", "suit": "HEARTS" } }
        }
      ]
    }
  ],
  "seed": 7,
  "hidden_ranges": {
    "1": {
      "weighted_hands": [
        {
          "weight": 1,
          "hand": {
            "type": "ordered",
            "slots": [
              { "strength_at_least": "A" },
              { "strength_at_most": "3" }
            ]
          }
        }
      ]
    }
  }
}
```

## Semantics

- `base_state` is an exact match state that anchors all public information and known private information.
- `hidden_ranges` overrides one or more players' hidden cards.
- `hidden_plays` overrides the current round's face-down card for one or more players.
- `completed_hidden_plays` overrides one or more already-completed face-down plays by `round_index` and `player`.
- when `base_state.current_hand` is present, `hidden_ranges` applies to the remaining hand contents inside that active hand
- when `base_state.current_hand` is present, `hidden_plays` applies only to the current round's face-down play
- when `base_state.current_hand` is present, `completed_hidden_plays` applies only to completed rounds already present in that active hand
- when `base_state.current_hand` is absent, `hidden_ranges` applies to the full 3-card hands that will be dealt next
- `pending_hand` is used only when `base_state.current_hand` is absent
- `pending_hand.turnup` is currently exact, not ranged
- each player's remaining hand size is inferred from the base state
- if `hidden_ranges` is empty or omitted, the resolved state is just the normalized exact `base_state`
- the resolver samples an exact legal replacement hand from the weighted range specification
- unresolved cards are drawn from the remaining legal deck after accounting for:
  - turnup
  - current cards on the table
  - fixed hands of players whose ranges are not being overridden
- in pre-deal mode, any player with no explicit range is sampled uniformly from the remaining legal deck
- cards are assigned back onto the original hidden-hand card ids after resolution
- exact hand patterns are compared as unordered sets, but resolved cards are written back in increasing Truco strength order before reusing the original ids
- in pre-deal mode, resolved cards receive generated ids of the form `p{player}c{index}`
- hidden-play overrides preserve the existing played-card id and visibility while replacing only rank/suit
- completed-round hidden-play overrides preserve the existing played-card id, visibility, and stored round outcome
- completed-round hidden-play overrides are inference, not history rewriting: they must keep the recorded `winner` of that completed round unchanged
- under the current Truco rules, that winner consistency is already implied by valid completed-round visibility history

The serialized `base_state` shape is defined by
[`../engine/schemas/match-state.schema.json`](../engine/schemas/match-state.schema.json),
which in turn references the exact hand
[`GameState`](../engine/schemas/game-state.schema.json). Exploration fixture
expectations are recursive subsets of the resolved `MatchState`, not complete
state documents.

## Weighted Hands

Each player range currently consists of `weighted_hands`.

Each weighted hand option has:

- `weight`
- `hand`

If multiple concrete hands satisfy a single weighted option, they all inherit that option's weight.

If two weighted options expand to the same exact hidden hand, their weights add implicitly because both branches remain eligible during sampling.

When several players have ranges at once, the resolver samples a joint assignment over compatible hands and multiplies the option weights across players.

Joint assignments that reuse the same exact card for more than one player are illegal and must be rejected.

## Hand Patterns

### Exact

Use `exact` when a range branch names a precise remaining hand.

```json
{
  "type": "exact",
  "cards": [
    { "rank": "A", "suit": "HEARTS" },
    { "rank": "2", "suit": "CLUBS" }
  ]
}
```

### Ordered

Use `ordered` when the range is easier to describe by relative hand strength.

Slots are interpreted from weakest to strongest using current Truco card strength under the known turnup.

```json
{
  "type": "ordered",
  "slots": [
    { "strength_at_least": "A" },
    { "strength_at_most": "3" }
  ]
}
```

This lets the exploration layer express statements like:

- the weaker remaining card is Ace-strength or better
- the stronger remaining card is at most a 3

## Card Constraints

The current executable subset supports:

- `exact`
- `allowed_ranks`
- `allowed_suits`
- `is_manilha`
- `strength_at_least`
- `strength_at_most`

These constraints are conjunctive.

That means a slot can simultaneously require, for example:

- `allowed_ranks`
- `allowed_suits`
- `is_manilha`

and all of them must hold for the card to match.

`hidden_plays.weighted_cards[*].card` uses the same single-card constraint language.

`completed_hidden_plays[*].weighted_cards[*].card` uses the same single-card constraint language.

## Current Scope

Implemented now:

- exact base match state
- identity resolution when no hidden ranges are provided
- weighted remaining-hand overrides
- pre-deal exact-turnup hand materialization from an idle match state
- active-round hidden-play identity overrides
- completed-round hidden-play identity overrides
- exact hand patterns
- ordered hand patterns
- seeded reproducible sampling
- stateful and stateless service routes

Not implemented yet:

- ranged turnup sampling before the hand starts
- automatic posterior reweighting from observed actions
- polished human-friendly notation / DSL

## Future Direction

The likely long-term architecture is:

1. exact engine state
2. exploration spec
3. optional human-friendly notation that compiles into the exploration spec
4. later, inference layers that update weighted ranges from observed actions

That keeps the engine exact while still allowing poker-style posterior ranges and exploratory state loading.
