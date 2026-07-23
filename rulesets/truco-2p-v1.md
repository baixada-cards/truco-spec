# Baixada Two-Player Truco Rules

Ruleset identifier: `truco-2p-v1`

This document defines Baixada's two-player *truco paulista* variant. It does
not claim to define every regional or social form of Truco.

## Objective

- Win the match by reaching 12 points before the other player.
- Points are scored by winning hands.

## Deck

- The deck has 40 cards.
- The ranks, from lowest to highest among non-manilhas, are `4`, `5`, `6`, `7`, `Q`, `J`, `K`, `A`, `2`, `3`.
- The suits are diamonds, spades, hearts, and clubs.

## Start Of A Hand

- Each player receives 3 cards.
- One turnup card is revealed and does not belong to either player.
- The turnup card defines the manilha rank for that hand.

## Manilhas

- The manilha rank is the next rank after the turnup rank in this circular order:
  - `4 -> 5 -> 6 -> 7 -> Q -> J -> K -> A -> 2 -> 3 -> 4`.
- Example: if the turnup is `A`, the manilhas are the four `2`s.
- Any manilha beats any non-manilha.
- Among non-manilhas, suit does not matter.
- Two non-manilhas of the same rank are tied even if their suits differ.
- If both played cards are manilhas, suit breaks the tie.
- The suit order from lowest to highest is:
  - diamonds,
  - spades,
  - hearts,
  - clubs.

## Deal And Lead

- The deal rotates after every hand.
- The player to the dealer's left leads the first round of the hand.

## Structure Of A Hand

- A hand consists of up to 3 rounds.
- Each round, both players play one card.
- A player wins the hand as soon as it is certain that the other player can no longer win the best-of-three contest.
- The winner of the hand scores the current value of the hand.

## Legal Plays

- On your turn, you may:
  - play one card face up,
  - play one card face down, except in the first round,
  - raise the hand value if no raise is currently awaiting an answer,
  - answer a pending raise.

## Face-Up And Face-Down Cards

- A face-up card uses its normal strength.
- A face-down card is not allowed in the first round.
- A face-down card is allowed only from the second round onward.
- A face-down card never beats a face-up card.
- If both played cards in a round are face down, the round is a tie.
- If one card is face up and the other is face down, only the face-up card can win the round.
- A face-down card stays unrevealed for the rest of the hand.

## Winning A Round

- After both players have played a card, the round is resolved.
- The stronger eligible card wins the round.
- If the two eligible cards are equal in strength, the round is a tie.

## Leading The Next Round

- The winner of a round leads the next round.
- If a round is tied, the player who led that round also leads the next round.

## Winning A Hand

- If one player wins the first two rounds, that player wins the hand.
- If each player wins one round, the third round decides the hand.
- If one player wins one round and another round is tied, the player who won the non-tied round wins the hand.
- If the first round is tied, the winner of the second non-tied round wins the hand.
- If all three rounds are tied, the player who led the first round wins the hand.

## Hand Value And Raises

- A hand starts worth 1 point.
- The raise ladder is `1 -> 3 -> 6 -> 9 -> 12`.
- A raise asks the other player to choose one of:
  - accept the new value,
  - fold the hand,
  - re-raise to the next value, if one exists.
- If the raise is accepted, the hand continues at the new value.
- If the raise is declined, the hand ends immediately and the player who made the last raise wins the hand at the previously accepted value.
- No raise above 12 is allowed.

## Mão De Onze

- If a player starts a hand with 11 points, that hand is played under mão de onze rules.
- In a mão de onze hand, raises are not allowed.
- The player with 11 points chooses before normal play begins:
  - play the hand for 3 points,
  - or fold immediately and concede 1 point.
- If both players start the hand with 11 points, the hand is played for 3 points with no raises.

## Match End

- A player wins the match immediately upon reaching 12 or more points.

## Hidden Information

- Your hand is hidden from the other player until cards are played.
- The turnup card is public.
- Cards played face up remain public.
- Cards played face down remain hidden.
