# Deal

This aspect covers pre-deal notation that compiles into:

- `pending_hand`
- `hidden_ranges`

Current scope:

- `deal(turnup=As, opp=[>=A, >=2, <=3])`
- `deal(turnup=As, opp={As, 2c}@1 | {4d, 5d}@2)`
- `seed=19` + `deal(...)` + `hidden(...)`
- `deal(...)` merged with a later `hero = {...}` range statement
- malformed `deal(...)` arguments fail explicitly
- a second `deal(turnup=...)` in the same script is a conflict
