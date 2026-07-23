# Raises

## Goal

Capture the full raise ladder and the legal and illegal responses to a pending raise.

## Scenario Seeds

- The opening raise from 1 to 3 is legal when no raise is pending.
- A raise can be accepted and the hand continues at the new value.
- Accepting a raise does not reset raise ownership; the player who made the accepted raise cannot immediately raise again before the opponent acts.
- A raise can be declined and the hand ends immediately.
- A raised hand can be re-raised by the other player to the next step in the ladder.
- The raise ladder progresses through 1, 3, 6, 9, and 12.
- A raise to 12 is legal when 9 has already been accepted.
- A player cannot raise to a value that is not the next step in the ladder.
- The same player cannot raise twice in a row without the opponent answering first.
- After a raise is accepted, the next legal raise opportunity belongs to the other player.
- No raise is allowed after the hand is already at 12.
- When a raise is pending, only the legal responses to that raise should be available.
- Mirror the raise, accept, decline, and re-raise flow from both players' perspectives.
- An unanswered raise should not coexist with ordinary card-play actions.
