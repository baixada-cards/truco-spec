# Ranges

This aspect covers notation that compiles into `hidden_ranges`.

Current scope:

- ordered hand expressions like `[>=A, <=3]`
- exact hand expressions like `{As, 2c}`
- weighted branch unions like `{As, 2c}@1 | {4d, 5d}@2`
- rank-class predicates like `A*`
- rank-set slot predicates like `[rank in {A,2,3}, <=3]`
- combined rank-class and suit filters like `[A* & suit in {SPADES, CLUBS}, <=3]`
- conjunctive slot predicates like `[rank in {A,2,3} & suit in {SPADES, CLUBS}, <=3]`
- alias resolution for `hero`, `villain`, `me`, and `opp`
