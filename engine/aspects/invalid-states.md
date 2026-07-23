# Invalid States

## Goal

Capture impossible starting states that the engine must reject immediately when loading a fixture.

## Scenario Seeds

- The same player has already won the first two rounds, but the hand still has a current round and a next player.
- The current round leader and `next_player` disagree with the recorded plays.
- The number of cards still in hand is inconsistent with the completed rounds and current round.
- A pending raise exists during mão de onze.
- A hidden play appears in the first round.
- A live hand exists although the match is already decided (a player on 12).
- The recorded first round was led by the dealer, or a later round's leader breaks the winner-leads chain.
- A single player is on 11 mid-hand at `hand_value` 1 with no pending decision.
- Two physical cards share the same card `id`.
- `hand_value` is not one of the raise-ladder values.
