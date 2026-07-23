# Hidden Plays

This aspect covers the identity of face-down cards already present in the active hand, both in the current round and in completed rounds.

Initial scenario targets:

- override the current round's face-down play exactly
- override a completed round's face-down play exactly
- combine a hidden-play override with a remaining-hand range for the same player
- reject hidden-play overrides when there is no active hand
- reject hidden-play overrides when the specified player has no hidden current-round play
- reject completed-round overrides when the specified round/player has no hidden play
