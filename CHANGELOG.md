# Changelog

All notable changes to the contract bundle are recorded here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and releases follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Documentation

- Exploration contract: added "Sampling Determinism", recording that the seeded
  weighted-branch fixtures pin which branch each seed selects, and that those
  selections depend on the reference engine's `rand` version (0.9 changed
  small-range integer sampling, so the same seed and weights draw differently).
  Notes what this means for non-Rust implementers and that changing the
  sampling algorithm is a breaking fixture change.

## [1.0.0-rc.1] - 2026-07-23

### Added

- Plain-language rules for the `truco-2p-v1` variant.
- Engine, exploration, and notation contracts.
- JSON Schemas and executable fixture corpora.
- Deterministic manifests and an independent validation suite.

[Unreleased]: https://github.com/baixada-cards/truco-spec/compare/v1.0.0-rc.1...HEAD
[1.0.0-rc.1]: https://github.com/baixada-cards/truco-spec/releases/tag/v1.0.0-rc.1
