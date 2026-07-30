# Weighted Branches

This aspect covers weighted alternatives inside a single player's range.

Initial scenario targets:

- zero-weight branches are ignored
- multiple exact branches are sampled reproducibly with a seed
- two branches that describe the same exact hand both contribute weight

The seeded fixtures here record *which* branch each seed selects, and those
selections depend on the reference implementation's RNG. See "Sampling
Determinism" in `../CONTRACT.md` before changing the engine's `rand` version or
porting these fixtures to another language.
