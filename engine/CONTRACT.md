# Engine Contract

## Purpose

This document defines the contract that every engine implementation should expose to the fixture runner.

The fixture corpus is not tied to HTTP, gRPC, or any other transport. Implementations may be wrapped in a subprocess adapter, an in-process binding, or a network service, as long as they honor the same contract.

## Conceptual Operations

Every engine implementation should support these conceptual operations:

- load a complete deterministic state
- reject an invalid state with a stable error code
- enumerate legal actions for a specific player
- apply an action to the current state
- reject an invalid action with a stable error code
- return the normalized public state

## Canonical Entities

### Player

- `0` or `1`

### Score

```json
{
  "0": 0,
  "1": 0
}
```

### Card

```json
{
  "id": "p0c0",
  "rank": "7",
  "suit": "DIAMONDS"
}
```

Rules:

- `id` is unique within the fixture
- `rank` is one of `4`, `5`, `6`, `7`, `Q`, `J`, `K`, `A`, `2`, `3`
- `suit` is one of `DIAMONDS`, `SPADES`, `HEARTS`, `CLUBS`

### Completed Round Summary

```json
{
  "leader": 0,
  "winner": null
}
```

Rules:

- `winner` is `0`, `1`, or `null`
- `null` means the round was tied

### Current Round Play

```json
{
  "player": 0,
  "visibility": "up",
  "card": {
    "rank": "7",
    "suit": "DIAMONDS"
  }
}
```

Rules:

- `visibility` is `up` or `down`
- if `visibility` is `up`, public state includes `rank` and `suit`
- if `visibility` is `down`, public state must not reveal the hidden card identity
- fixture `initial_state` may still include the real hidden card internally so the engine can load the state deterministically

### Pending Raise

```json
{
  "raised_by": 0,
  "to": 3,
  "previous_value": 1
}
```

Rules:

- `raised_by` is the player who made the last unanswered raise
- `to` is the proposed hand value
- `previous_value` is the currently accepted hand value before the raise is accepted

### Pending Decision

```json
{
  "type": "mao_de_onze",
  "player": 0
}
```

Rules:

- `type` identifies the decision family
- `player` is the player who must choose
- while this decision is pending, the only legal actions are the decision responses for that player

## Canonical Initial State

The current canonical `initial_state` is:

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
      { "id": "p0c1", "rank": "6", "suit": "CLUBS" }
    ],
    "1": [
      { "id": "p1c1", "rank": "5", "suit": "SPADES" },
      { "id": "p1c2", "rank": "4", "suit": "DIAMONDS" }
    ]
  },
  "completed_rounds": [
    {
      "leader": 0,
      "winner": 0
    }
  ],
  "current_round": {
    "leader": 0,
    "plays": []
  },
  "last_raised_by": null,
  "pending_raise": null,
  "pending_decision": null
}
```

Interpretation rules:

- `hands` list only cards still held by the players
- cards used in prior rounds are omitted from `hands`
- `completed_rounds` summarize earlier rounds in the current hand
- `current_round` contains only the plays already made in the active round
- `next_player` is the player expected to act now
- `hand_value` is the currently accepted value of the hand, not the pending proposed value
- `last_raised_by` records who most recently escalated the hand value and constrains who may raise next
- `pending_decision` is used for pre-play branches such as `mão de onze` when exactly one player is on 11

An engine must reject an initial state if it is internally inconsistent or impossible under the rules.

The normative serialized shape is
[`schemas/game-state.schema.json`](schemas/game-state.schema.json). JSON
Schema validates the transport shape; the consistency rules below remain
semantic engine requirements.

Examples:

- a hand continues even though a player has already won it
- `next_player` conflicts with the round history
- a hidden card appears in the first round
- a player still holds too many or too few cards for the recorded history
- a pending raise exists in a state where raises are forbidden
- a pending `mão de onze` decision and a pending raise both exist at once
- a live hand exists although a player already reached 12 points
- a recorded round-leader chain contradicts the rules (the dealer led the first round, or a later round is not led by the previous round's winner-or-leader)
- a one-player-at-11 hand is worth 1 with no pending decision (accepting makes it 3; folding ends it)
- `hand_value` is not a raise-ladder value
- two physical cards share the same `id`

## Canonical Public State

The normalized public state returned by an engine should use this shape:

```json
{
  "next_player": 1,
  "hand_value": 1,
  "hand_winner": null,
  "match_winner": null,
  "score": { "0": 0, "1": 0 },
  "completed_rounds": [
    {
      "leader": 0,
      "winner": null
    }
  ],
  "current_round": {
    "leader": 0,
    "plays": [
      {
        "player": 0,
        "visibility": "up",
        "card": {
          "rank": "7",
          "suit": "DIAMONDS"
        }
      }
    ]
  },
  "pending_raise": null,
  "pending_decision": null
}
```

Normalization rules:

- `hand_winner` is `0`, `1`, or `null`
- `match_winner` is `0`, `1`, or `null`
- tied completed rounds are represented as `"winner": null`
- hidden cards in `current_round.plays` expose only `player` and `visibility`
- `pending_decision` is either `null` or a normalized decision object
- internal engine details, caches, derived card strengths, and implementation-specific objects must not appear

The complete normalized response is defined by
[`schemas/public-state.schema.json`](schemas/public-state.schema.json).
Fixture steps deliberately use
[`schemas/partial-public-state.schema.json`](schemas/partial-public-state.schema.json)
because `assert_state` and `assert_export_round_trip` are subset assertions.

## Canonical Actions

### Play Face Up

```json
{
  "type": "play_face_up",
  "card_id": "p0c0"
}
```

### Play Face Down

```json
{
  "type": "play_face_down",
  "card_id": "p0c0"
}
```

### Raise

```json
{
  "type": "raise",
  "to": 3
}
```

### Accept Raise

```json
{
  "type": "accept_raise"
}
```

### Fold

```json
{
  "type": "fold"
}
```

### Accept Eleven

```json
{
  "type": "accept_eleven"
}
```

### Fold Eleven

```json
{
  "type": "fold_eleven"
}
```

### Concede Hand

```json
{
  "type": "concede_hand"
}
```

## Error Codes

Invalid actions should fail with stable machine-oriented error codes rather than engine-specific prose.

Examples:

- `INVALID_INITIAL_STATE`
- `HAND_ALREADY_DECIDED`
- `ACT_OUT_OF_TURN`
- `CARD_NOT_IN_HAND`
- `HIDE_NOT_ALLOWED_IN_FIRST_ROUND`
- `RAISE_NOT_ALLOWED`
- `INVALID_RAISE_TARGET`
- `NO_PENDING_RAISE`
- `NO_PENDING_ELEVEN_DECISION`
- `RAISE_PENDING` (a card play arrives while a raise awaits an answer)
- `DECISION_PENDING` (a card play arrives while a `mão de onze` decision is open)
- `INVALID_PLAYER`
- `SERIALIZATION_FAILED`

Exact coverage can grow later, but new fixtures should prefer error codes from the start.
