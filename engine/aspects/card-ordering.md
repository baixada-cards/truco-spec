# Card Ordering

## Goal

Capture the card-strength rules independently from raises, scoring, and most hand-flow concerns.

## Scenario Seeds

- Two non-manilhas of the same rank but different suits tie.
- A stronger non-manilha beats a weaker non-manilha.
- Any manilha beats any non-manilha.
- Between two manilhas, clubs beats hearts, hearts beats spades, and spades beats diamonds.
- The same visible card ordering should produce the same round result regardless of unused cards in hand.
