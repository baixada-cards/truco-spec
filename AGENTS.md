# Agent instructions

## Scope

This repository is the public, implementation-neutral contract for Baixada's
two-player Truco rules, engine behavior, exploration semantics, and notation.
Implementation-specific code belongs in a consumer repository.

## Contract discipline

- Treat `rulesets/truco-2p-v1.md` as the canonical prose definition of
  `truco-2p-v1`.
- Keep each surface's `CONTRACT.md`, `ASPECTS.md`, schemas, and fixtures aligned.
- Never change the meaning of a published ruleset identifier. Introduce a new
  identifier for a material game-rule change.
- Prefer additive schema evolution. A breaking schema or fixture change
  requires a major repository release.
- Fixture IDs match their paths below the corresponding `fixtures/` directory.
- Use stable, implementation-neutral error and operation names.
- Do not add production engine, service, frontend, solver, or provider code.
- Consumers pin a signed release or exact commit; documentation must not
  recommend a moving branch as a dependency.

## Workflow

1. State the rule or contract decision in prose.
2. Update the relevant aspect and contract documents.
3. Update the JSON Schema when the transport shape changes.
4. Add the smallest fixtures that distinguish the intended behavior.
5. Run `make manifest` after the payload is final.
6. Run `make check` before committing.

Use signed commits. Keep dependencies locked and preserve the seven-day minimum
release-age policy in `pyproject.toml`.
