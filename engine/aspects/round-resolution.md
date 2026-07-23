# Round Resolution

## Goal

Capture how individual rounds are scored once each player has acted, including ties, hidden cards, and round-ending edge cases.

## Scenario Seeds

- A higher non-manilha beats a lower non-manilha.
- Two non-manilhas of the same rank tie, even if their suits differ.
- Any manilha beats any non-manilha.
- Between two manilhas, suit order decides the round.
- A face-up card beats a face-down card.
- Two face-down cards produce a tied round.
- A round ends immediately when a player folds to a raise.
- A round cannot resolve before both players have either played a card or a fold ends the round.
- A tied round does not produce a winner.
- A won round records the winning player and the leading player for that round.
- A round with one face-up card and one hidden card should resolve according to the visible card only.
- The same visible card matchup should resolve the same way regardless of which unused cards remain in hand.
- A round cannot continue after it has already ended.
