# Fixture Workflow

## Goal

This workflow is meant to support staged parallel work:

1. agree on the rules,
2. agree on the fixture format,
3. break coverage into aspects,
4. expand each aspect into scenario inventories,
5. turn approved scenarios into executable fixtures.

## Recommended Stages

### Stage 1: Rules Lock-In

- update the matching document under `rulesets/` until the target variant is
  stable enough to test
- do not fan out fixture generation while a rule area is still unsettled

### Stage 2: Aspect Planning

- update `engine/ASPECTS.md`
- create or expand one file under `engine/aspects/` per aspect
- keep these files high-level and human-readable

### Stage 3: Scenario Expansion

- turn each aspect document into a list of scenario seeds
- prefer one rule question per scenario seed
- identify edge cases, mirror cases, and invalid-action cases explicitly

### Stage 4: Fixture Authoring

- turn each approved scenario seed into one or more JSON fixture files under `engine/fixtures/<aspect>/`
- keep file names descriptive and stable
- validate every new fixture against the JSON schema
- when the starting state is impossible, author an invalid-state fixture with `expect_initial_state_error` instead of `steps`

### Stage 5: Runner Integration

- make the runner load fixtures in any order
- treat each fixture as self-contained
- compare only normalized public state and stable error codes

## Parallelization Strategy

The safest unit of parallel work is one aspect directory at a time.

Examples:

- one contributor owns `engine/aspects/card-ordering.md`
- another owns `engine/aspects/hidden-cards.md`
- later, different contributors can author files under `engine/fixtures/card-ordering/` and `engine/fixtures/hidden-cards/`

Within one aspect, split by scenario families when the write set is disjoint.

## Subagent Handoff Pattern

For scenario-expansion work:

- assign one aspect markdown file
- ask for a numbered scenario inventory
- ask for gaps, variants, and invalid-action cases
- do not ask for JSON yet

For fixture-authoring work:

- assign one fixture directory
- provide the aspect markdown file as the source of truth
- ask for concrete JSON files only
- require compliance with the schemas and naming rules
- distinguish invalid actions from invalid initial states explicitly

## Review Checklist

Before approving a new aspect or fixture set, check:

- does it test one primary rule idea cleanly
- does it avoid random dealing
- does it avoid hidden assumptions not stated in the matching `rulesets/`
  document
- does it use normalized public-state assertions
- does it use stable error codes for invalid actions
- does it use `expect_initial_state_error` for impossible states
- is it placed in the correct aspect directory
