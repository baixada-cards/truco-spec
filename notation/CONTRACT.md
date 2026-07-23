# Notation Fixture Contract

## Purpose

Notation fixtures define how the shorthand exploration language compiles into the exploration JSON contract.

They do not execute the engine directly. They only test parser behavior.

## Top-Level Shape

```json
{
  "id": "ranges/opp-ordered-range",
  "ruleset": "truco-2p-v1",
  "context": {
    "human_player": 0,
    "bot_player": 1
  },
  "notation": "opp = [>=A, <=3]",
  "expect_fragment": {
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
}
```

## Context

`context` supplies the player aliases used by the notation language:

- `hero` / `h` / `p0` -> player `0`
- `villain` / `v` / `p1` -> player `1`
- `me` -> `context.human_player`
- `opp` / `opponent` / `bot` -> `context.bot_player`

## Supported Executable Subset

Current fixtures cover:

- ordered hand ranges like `opp = [>=A, <=3]`
- exact hands like `hero = {As, 2c}`
- weighted alternatives like `{As, 2c}@1 | {4d, 5d}@2`
- rank-class shorthands like `A*`
- current hidden-play constraints like `hidden(opp) = manilha`
- weighted hidden-play alternatives like `hidden(opp) = manilha@2 | As@1`
- weighted completed hidden-play alternatives like `hidden(round=0, player=hero) = As@2 | 2c@1`
- rank-set predicates like `opp = [rank in {A,2,3}, <=3]`
- suit-set predicates like `hidden(opp) = suit in {SPADES, CLUBS}`
- conjunctive predicates like `A* & suit in {SPADES, CLUBS}`
- completed hidden-play constraints like `hidden(round=0, player=hero) = As`
- pre-deal statements like `deal(turnup=As, opp=[>=A, >=2, <=3])`
- weighted pre-deal hand branches like `deal(turnup=As, opp={As, 2c}@1 | {4d, 5d}@2)`
- seed statements like `seed=13`
- multi-line scripts that merge several statements into one fragment
- mixed scripts like `seed=19` + `deal(...)` + `hidden(...)`
- mixed scripts like `seed=23` + current `hidden(...)` + completed `hidden(round=..., player=...)`
- blank lines and `#` comments inside scripts
- workflow scripts that combine both-player ranges, hidden plays, and pre-deal setup

## Error Model

Error fixtures assert:

- `code`
- `message_contains`
- `line`
- `column`

The current stable code for parser failures is `NOTATION_PARSE_ERROR`.

For multi-line scripts, conflicting assignments are rejected instead of silently overwriting:

- a second `seed=...`
- a second `deal(turnup=...)`
- a second assignment to the same player's `hidden_ranges`
- a second assignment to the same player's `hidden_plays`
- a second assignment to the same completed hidden-play target `(round_index, player)`

Blank lines and `#` comments are ignored before statement splitting.
