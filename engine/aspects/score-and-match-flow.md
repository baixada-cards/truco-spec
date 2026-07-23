# Score And Match Flow

## Goal

Capture how hand wins change score, when the match ends, and how `mão de onze` changes the flow.

## Scenario Seeds

- A normal hand win awards 1 point.
- A raised hand win awards the current accepted hand value.
- A declined raise awards the previously accepted hand value to the last raiser.
- Conceding the hand awards the current accepted hand value to the opponent.
- Conceding while a raise or re-raise is pending awards the implicitly accepted value (the pending raise's `previous_value`) — the same amount a fold would award, never less.
- Reaching 12 ends the match immediately after score is applied.
- A player on 11 must choose between playing the hand for 3 points and folding for 1 point.
- If only one player is on 11, that player owns the `mão de onze` decision even when the other seat opens the hand.
- A player on 11 cannot raise.
- If both players start on 11, the hand starts at 3 points, no `mão de onze` decision node is created, and raises are still disallowed.
- A hand can end in the middle of the third round once the outcome is already decided.
- A tied first round followed by one won round should award the hand correctly.
- A one-win, one-tie sequence should produce the right hand winner and score.
- A first-two-rounds win should end the hand before a third round is needed.
- A match-winning hand should not allow any further actions after the score is applied.
- The winner of the hand should receive the score even when the deciding action is a fold.
