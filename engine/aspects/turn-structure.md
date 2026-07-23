# Turn Structure

## Goal

Capture who acts when, how turns advance within a round, and how pending raises affect the next legal move.

## Scenario Seeds

- The dealer's left neighbor leads the first round.
- After a round is won, the winning player leads the next round.
- After a tied round, the same player leads the next round.
- The non-leading player acts second in a round.
- The same player cannot act twice in a row during a normal round.
- A player cannot act out of turn.
- A player cannot answer a raise when no raise is pending.
- A player cannot make a new raise while an answer is pending.
- A player can accept a pending raise.
- A player can fold in response to a pending raise.
- A player can concede the hand on any live turn, including ordinary card-play turns and pending decision nodes.
- A player can re-raise in response to a pending raise when a higher value exists.
- A player cannot re-raise above 12.
- A player cannot raise twice in a row without the other player responding.
- After a raise is accepted, the original raiser resumes ordinary play but cannot immediately start the next raise escalation.
- The active turn passes back to the correct player after accept, fold, and re-raise responses.
- Turn order resets cleanly at the start of a new round after the previous round ends.
