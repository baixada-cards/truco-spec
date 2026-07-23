# Engine Fixture Spec

## Purpose

This directory defines a language-agnostic fixture corpus for the 2-player Truco engine.

The goals are:

- keep fixtures deterministic and easy to read,
- make them executable against any engine implementation,
- separate high-level scenario planning from concrete JSON fixtures,
- let different contributors work in parallel without stepping on each other.

Related documents:

- `engine/CONTRACT.md`
  - canonical entities, operations, and normalized public state
- `engine/WORKFLOW.md`
  - recommended authoring and delegation workflow
- `engine/ASPECTS.md`
  - master list of rule areas to cover
- `engine/schemas/fixture.schema.json`
  - machine-checkable schema for fixture files
- `engine/schemas/game-state.schema.json`
  - complete exact state for one active hand
- `engine/schemas/match-state.schema.json`
  - complete exact match state used by exploration and persistence boundaries
- `engine/schemas/public-state.schema.json`
  - complete normalized public state returned by an engine
- `engine/schemas/partial-public-state.schema.json`
  - subset shape used only by partial fixture assertions

## Directory Layout

- `engine/ASPECTS.md`
  - master list of rule areas that need coverage
- `engine/aspects/*.md`
  - high-level scenario lists for one aspect at a time
- `engine/fixtures/<aspect>/*.json`
  - concrete executable fixtures grouped by aspect
- `engine/schemas/*.json`
  - JSON schemas for fixture validation

## Fixture Shape

Each fixture is a single JSON file with this top-level structure:

```json
{
  "fixture_version": "engine-fixture/v1",
  "id": "hidden-cards/cannot-hide-first-round",
  "ruleset": "truco-2p-v1",
  "description": "Face-down play is illegal in the first round.",
  "initial_state": {},
  "steps": []
}
```

Invalid-state fixtures use this top-level structure instead:

```json
{
  "fixture_version": "engine-fixture/v1",
  "id": "invalid-states/hand-continues-after-two-round-win",
  "ruleset": "truco-2p-v1",
  "description": "A hand cannot continue after the same player has already won the first two rounds.",
  "initial_state": {},
  "expect_initial_state_error": "HAND_ALREADY_DECIDED"
}
```

## `initial_state`

`initial_state` describes a complete deterministic current game state.

Its serialized shape is defined by
`engine/schemas/game-state.schema.json`. The schema checks structure; the
engine contract and invalid-state fixtures define cross-field game legality.

It may represent:

- the very start of a hand,
- the middle of a hand,
- a state with completed rounds already recorded,
- a state with a raise currently awaiting an answer,
- a state with a pending `mão de onze` decision when exactly one player is on 11.

Core required fields:

- `dealer`
- `next_player`
- `score`
- `hand_value`
- `turnup`
- `hands`
- `completed_rounds`
- `current_round`
- `pending_raise`

Optional fields:

- `last_raised_by`
- `pending_decision`

Suggested shape:

```json
{
  "dealer": 1,
  "next_player": 0,
  "score": { "0": 0, "1": 0 },
  "hand_value": 1,
  "turnup": { "rank": "A", "suit": "SPADES" },
  "hands": {
    "0": [
      { "id": "p0c0", "rank": "7", "suit": "DIAMONDS" },
      { "id": "p0c1", "rank": "6", "suit": "CLUBS" },
      { "id": "p0c2", "rank": "4", "suit": "HEARTS" }
    ],
    "1": [
      { "id": "p1c0", "rank": "7", "suit": "CLUBS" },
      { "id": "p1c1", "rank": "5", "suit": "SPADES" },
      { "id": "p1c2", "rank": "4", "suit": "DIAMONDS" }
    ]
  },
  "completed_rounds": [],
  "current_round": {
    "leader": 0,
    "plays": []
  },
  "last_raised_by": null,
  "pending_raise": null,
  "pending_decision": null
}
```

`hands` always contain the cards still held by each player at this exact moment.

## Naming Rules

- The fixture `id` must match the file path below `engine/fixtures/`, without the `.json` suffix.
- Use lowercase kebab-case for aspect names and file names.
- Each fixture file should test one primary rule question.
- One fixture file must belong to exactly one aspect directory.

## `steps`

Each step is one of:

- `assert_legal_actions`
- `apply_action`
- `assert_state`
- `assert_rejected_action`

### `assert_legal_actions`

Checks the currently legal actions for a player.

```json
{
  "op": "assert_legal_actions",
  "player": 0,
  "must_include": [
    { "type": "play_face_up", "card_id": "p0c0" }
  ],
  "must_exclude": [
    { "type": "play_face_down", "card_id": "p0c0" }
  ]
}
```

Action ordering is not significant. `must_include` and `must_exclude` are set-based checks.

### `apply_action`

Applies one action to the current engine state.

```json
{
  "op": "apply_action",
  "player": 0,
  "action": { "type": "play_face_up", "card_id": "p0c0" }
}
```

### `assert_state`

Checks a partial normalized public state.

```json
{
  "op": "assert_state",
  "expect": {
    "next_player": 1,
    "hand_value": 1,
    "hand_winner": null,
    "completed_rounds": []
  }
}
```

`assert_state` is a partial match, not necessarily a full state dump.
Accordingly, assertions use `partial-public-state.schema.json`; complete
engine responses use `public-state.schema.json`.

### `assert_export_round_trip`

Exports the current engine state, imports it again, and checks a partial
normalized public-state fragment after the round trip.

```json
{
  "op": "assert_export_round_trip",
  "expect": {
    "next_player": 1,
    "hand_value": 3,
    "pending_raise": null
  }
}
```

Use this operation when a scenario depends on preserving state that can be
lost or reconstructed incorrectly at a persistence boundary.

### `assert_rejected_action`

Checks that an attempted action is rejected with a stable error code.

```json
{
  "op": "assert_rejected_action",
  "player": 0,
  "action": { "type": "play_face_down", "card_id": "p0c0" },
  "error_code": "HIDE_NOT_ALLOWED_IN_FIRST_ROUND"
}
```

## Action Encoding

Supported action shapes are:

- `{ "type": "play_face_up", "card_id": "p0c0" }`
- `{ "type": "play_face_down", "card_id": "p0c0" }`
- `{ "type": "raise", "to": 3 }`
- `{ "type": "accept_raise" }`
- `{ "type": "fold" }`
- `{ "type": "accept_eleven" }`
- `{ "type": "concede_hand" }`
- `{ "type": "fold_eleven" }`

The same `raise` action shape is used for the initial raise and for later re-raises. Context determines whether it is a raise or a re-raise.

## State Normalization

For cross-language compatibility, fixture assertions should only depend on normalized public outputs. The canonical field set is defined in `CONTRACT.md` and the public-state schema.

Typical fields include:

- `next_player`
- `hand_value`
- `hand_winner`
- `match_winner`
- `score`
- `completed_rounds`
- `pending_raise`
- `pending_decision`
- `current_round`

Do not require internal implementation details.

## Authoring Rules

- Keep one primary rule idea per fixture.
- Use explicit hands and explicit turnups. Do not use random dealing in fixtures.
- Prefer small scenarios that isolate one question.
- Group fixtures by aspect so coverage work can be split safely across parallel contributors.
- Use `assert_state` for normalized public state and `assert_rejected_action` for invalid-action behavior.
- Prefer stable error codes over engine-specific error messages.
- Use `expect_initial_state_error` when the state itself is impossible and must be rejected before any action is taken.
