# Engine Test Aspects

These are the main rule areas that should eventually have dedicated coverage.

## Card Model

- base rank ordering among non-manilhas
- ties between non-manilhas of the same rank and different suits
- manilha detection from the turnup
- suit ordering among manilhas
- manilha versus non-manilha precedence

## Turn Structure

- first leader from dealer position
- next leader after a won round
- next leader after a tied round
- legal actions at the start of a round
- legal actions while a raise is pending

## Hidden Cards

- hidden cards are illegal in the first round
- hidden cards are legal from the second round onward
- hidden card loses to face-up card
- hidden versus hidden produces a tied round
- hidden cards remain unrevealed

## Round Resolution

- visible card beats weaker visible card
- equal non-manilhas tie
- stronger manilha wins
- round result when one side hides
- round result when both sides hide

## Hand Resolution

- straight 2-0 hand wins
- 1-1 split goes to third round
- one win plus one tie wins the hand
- first-round tie followed by a win
- all three rounds tied

## Raises

- initial raise from 1 to 3
- accept raise
- decline raise
- re-raise ladder 3 to 6 to 9 to 12
- illegal same-side consecutive raise
- no raise above 12

## Score And Match Flow

- hand winner receives current hand value
- match ends at 12
- mão de onze disables raises
- mão de onze accept/play branch
- mão de onze fold branch
- both players on 11 auto-play for 3

## Errors And Invalid Actions

- invalid initial state rejection
- hand already decided but play continues
- next player inconsistent with current round history
- impossible card counts after recorded history
- pending raise in an illegal context
- playing a card you do not hold
- acting out of turn
- illegal hide in first round
- answering a raise when none is pending
- illegal raise amount
