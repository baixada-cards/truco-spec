# Truco Spec

The public, implementation-neutral contract for Baixada's two-player *truco
paulista*.

This repository answers three different questions:

1. Which game are we implementing?
2. Which states and operations must an engine support?
3. How do exploration and human-authored notation resolve into exact game
   states?

Implementations are conforming consumers. They do not silently redefine these
contracts.

## Repository layout

| Path | Purpose |
| --- | --- |
| [`rulesets/truco-2p-v1.md`](rulesets/truco-2p-v1.md) | Immutable plain-language rules for `truco-2p-v1` |
| [`engine/`](engine/) | Engine contract, public-state schemas, and executable fixtures |
| [`exploration/`](exploration/) | Hidden-information and partial-state exploration contract |
| [`notation/`](notation/) | Human-authored exploration notation contract |
| [`spec-manifest.json`](spec-manifest.json) | Versioned corpus metadata and deterministic payload hashes |
| [`VERSION`](VERSION) | Semantic version of this repository's contract bundle |

The fixture corpus is language-agnostic. Rust, TypeScript, Python, or another
implementation may consume it as long as that implementation reports
conformance without changing the fixtures in transit.

## Validate the corpus

The validation suite uses Python 3.12 or 3.13 and
[uv](https://docs.astral.sh/uv/). Dependencies are locked and releases newer
than seven days are excluded during resolution. Registry access goes through
[Socket Firewall Free](https://docs.socket.dev/docs/socket-firewall-free).

```sh
sfw uv sync --frozen --group dev
make check
```

`make check` validates formatting, JSON Schema conformance, fixture invariants,
and the deterministic release manifest.

After an intentional contract change, regenerate the manifest and run the full
suite:

```sh
make manifest
make check
```

## Consume a release

Consumers must pin a signed release tag or exact commit. Do not build against a
moving `main` branch.

For each pinned revision:

1. read `VERSION` and `spec-manifest.json`;
2. verify the payload hashes in `spec-manifest.json`;
3. execute the relevant fixture corpus in the consumer's own test suite;
4. record the pinned spec version or commit in that consumer's lock or release
   metadata.

The contract bundle is released directly from Git. It is not an npm, PyPI, or
crates.io package.

The first public line is released as `v1.0.0-rc.*`. It becomes `v1.0.0` only
after the engine, server, and web consumers all pass their conformance suites
against the same candidate.

`make release` creates a normalized source archive, a per-file release
inventory, and `SHA256SUMS` in `dist/`. The archive is intentionally
reproducible: CI builds it twice and requires byte-identical output. Consumers
should verify `SHA256SUMS` before trusting the embedded manifest.

## Versioning

Repository releases use Semantic Versioning:

- **major**: a breaking rules, schema, fixture, or interpretation change;
- **minor**: a backward-compatible capability or fixture addition;
- **patch**: a clarification or correction that preserves consumer behavior.

The `ruleset` identifier inside fixtures is stricter than the repository
version. Once published, the meaning of `truco-2p-v1` is immutable. A material
change to the game rules receives a new identifier such as `truco-2p-v2`, and
both versions may coexist during migration.

See each surface's `CONTRACT.md`, `ASPECTS.md`, and `WORKFLOW.md` before making
a behavioral change.

## License

The specifications, schemas, fixtures, and supporting documentation are
available under the [MIT License](LICENSE).
