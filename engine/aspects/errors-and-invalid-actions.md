# Errors And Invalid Actions

## Goal

Capture invalid moves that must be rejected while a fixture is otherwise loaded from a valid state.

## Scenario Seeds

- A player tries to play a card out of turn.
- A player tries to play a card they no longer hold.
- A player tries to hide a card in the first round.
- A player tries to answer a raise when no raise is pending.
- A player tries to raise to an illegal target value.
- A player tries to raise when raises are disallowed by `mão de onze`.
- The same player tries to raise twice in a row without the other side responding.
- A player tries to play a card after the hand has already ended.
- A player tries to act after the match has already ended.
- A player tries to fold when no raise is pending.
- A player tries to accept a raise that was not made by the opponent.
- A player tries to re-raise above 12.
- A player tries to use an action type that is not part of the contract.
