# Exploration Test Aspects

These are the main exploration-language areas that should eventually have dedicated coverage.

## Hidden Ranges

- identity resolution when no hidden ranges are supplied
- exact hidden remaining hand overrides
- ordered hidden remaining hand overrides
- conjunctive card constraints inside ordered slots
- range resolution that preserves public information
- range resolution that preserves hand sizes and card ids

## Nature Nodes

- start a fresh hand from an idle exact match state
- exact turnup specification before the hand starts
- one player specified, one player left to uniform chance
- both players left to uniform chance
- ranged full-hand specification before the hand starts

## Hidden Plays

- override the current round's single face-down play
- override a completed round's face-down play by `round_index` and `player`
- leave remaining private hand cards exact while overriding the hidden play
- combine a hidden-play override with a remaining-hand override for the same player
- reject hidden-play overrides when there is no active hand
- reject hidden-play overrides when the current round has no face-down play for that player
- reject completed-round overrides when the target round/player has no face-down play

## Weighted Branches

- zero-weight branches are ignored
- multiple exact branches with different weights
- overlapping branches
- deterministic sampling when a seed is provided

## Joint Ranges

- both players ranged at once
- incompatible joint assignments are rejected
- compatible assignments avoid duplicate-card collisions

## Errors

- exploration requires an active hand for hidden-hand overrides
- base states that fail engine validation are rejected
- impossible range specs produce no candidates
- invalid player identifiers are rejected

## Future Scope

- unresolved turnup / pre-deal nature nodes
- posterior reweighting from observed actions
- richer user-facing notation that compiles into the transport contract
