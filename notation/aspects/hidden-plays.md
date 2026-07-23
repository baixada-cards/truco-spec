# Hidden Plays

This aspect covers notation that compiles into:

- `hidden_plays`
- `completed_hidden_plays`

Current scope:

- `hidden(opp) = manilha`
- `hidden(round=0, player=hero) = As`
- `hidden(round=0, player=hero) = As@2 | 2c@1`
- `hidden(opp) = manilha@2 | As@1`
- `hidden(opp) = A* & suit in {SPADES, CLUBS}`
- `hidden(opp) = suit in {SPADES, CLUBS}`
- `hidden(opp) = manilha & suit in {SPADES, CLUBS}`
- multi-line scripts that mix current and completed hidden targets
- duplicate completed hidden targets in the same script are conflicts
