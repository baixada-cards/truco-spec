# Notation Fixtures

This directory defines the transport-neutral fixture corpus for the exploration notation language.

The goal is the same one we already use for the engine and exploration specs:

- write down executable expectations once
- validate the corpus with `pytest`
- run the same corpus against parser implementations in different languages

The fixtures and `CONTRACT.md` are canonical. Parser implementations may live
in Rust or any other language, but they conform to this corpus rather than
defining it.

## Layout

- `CONTRACT.md`: fixture contract for notation compilation
- `ASPECTS.md`: coverage map
- `PARITY.md`: mapping from notation features to exploration-contract features
- `aspects/`: planning docs for notation behavior
- `schemas/`: JSON Schema for fixture validation
- `fixtures/`: executable parser cases

## Outcome Model

Each fixture provides:

- a `context` with seat aliases like `me` and `opp`
- a raw `notation` string
- either:
  - `expect_fragment`, or
  - `expect_error`

Successful fixtures assert the exact compiled JSON fragment. Error fixtures assert stable error metadata like code, line, column, and message substring.

Notation scripts may also include blank lines and `#` comments. Those are ignored before compilation.

## Current Recommendation

The notation layer is now broad enough for the workflows we currently care about in the lab and exploration tooling.

So the near-term priority is not more syntax for its own sake. It is:

- keeping notation aligned with the exploration contract
- adding notation fixtures when real workflows expose a gap
- otherwise shifting project energy back toward the playable product

The notation surface should remain a practical authoring layer, not become a mini-language project detached from product needs.
