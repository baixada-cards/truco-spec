"""Validation tests for language-agnostic engine fixtures."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
SPECS_DIR = ROOT / "engine"
FIXTURES_DIR = SPECS_DIR / "fixtures"
SCHEMAS_DIR = SPECS_DIR / "schemas"
FIXTURE_SCHEMA_PATH = SCHEMAS_DIR / "fixture.schema.json"
GAME_STATE_SCHEMA_PATH = SCHEMAS_DIR / "game-state.schema.json"
PARTIAL_PUBLIC_STATE_SCHEMA_PATH = SCHEMAS_DIR / "partial-public-state.schema.json"
PUBLIC_STATE_SCHEMA_PATH = SCHEMAS_DIR / "public-state.schema.json"


def _load_json(path: Path) -> object:
    return json.loads(path.read_text())


def _fixture_paths() -> list[Path]:
    return sorted(FIXTURES_DIR.rglob("*.json"))


FIXTURE_PATHS = _fixture_paths()


def test_fixture_corpus_is_not_empty():
    assert FIXTURE_PATHS


@pytest.fixture(scope="module")
def fixture_schema() -> dict:
    return _load_json(FIXTURE_SCHEMA_PATH)


@pytest.fixture(scope="module")
def game_state_schema() -> dict:
    return _load_json(GAME_STATE_SCHEMA_PATH)


@pytest.fixture(scope="module")
def partial_public_state_schema() -> dict:
    return _load_json(PARTIAL_PUBLIC_STATE_SCHEMA_PATH)


@pytest.fixture(scope="module")
def public_state_schema() -> dict:
    return _load_json(PUBLIC_STATE_SCHEMA_PATH)


@pytest.fixture(scope="module")
def fixture_validator(fixture_schema: dict) -> Draft202012Validator:
    return Draft202012Validator(fixture_schema)


@pytest.fixture(scope="module")
def game_state_validator(game_state_schema: dict) -> Draft202012Validator:
    return Draft202012Validator(game_state_schema)


@pytest.fixture(scope="module")
def partial_public_state_validator(
    partial_public_state_schema: dict,
) -> Draft202012Validator:
    return Draft202012Validator(partial_public_state_schema)


@pytest.fixture(scope="module")
def public_state_validator(public_state_schema: dict) -> Draft202012Validator:
    registry = Registry().with_resource(
        public_state_schema["$id"], Resource.from_contents(public_state_schema)
    )
    return Draft202012Validator(public_state_schema, registry=registry)


def test_schemas_are_valid(
    fixture_schema: dict,
    game_state_schema: dict,
    partial_public_state_schema: dict,
    public_state_schema: dict,
):
    Draft202012Validator.check_schema(fixture_schema)
    Draft202012Validator.check_schema(game_state_schema)
    Draft202012Validator.check_schema(partial_public_state_schema)
    Draft202012Validator.check_schema(public_state_schema)


@pytest.mark.parametrize("fixture_path", FIXTURE_PATHS, ids=lambda path: path.stem)
def test_fixture_parses_as_json(fixture_path: Path):
    _load_json(fixture_path)


@pytest.mark.parametrize("fixture_path", FIXTURE_PATHS, ids=lambda path: path.stem)
def test_fixture_matches_schema(
    fixture_path: Path,
    fixture_validator: Draft202012Validator,
):
    fixture = _load_json(fixture_path)
    errors = sorted(fixture_validator.iter_errors(fixture), key=str)
    assert errors == [], "\n".join(
        f"{fixture_path}: {'/'.join(map(str, error.path)) or '<root>'}: {error.message}"
        for error in errors
    )


@pytest.mark.parametrize("fixture_path", FIXTURE_PATHS, ids=lambda path: path.stem)
def test_initial_state_matches_game_state_schema(
    fixture_path: Path,
    game_state_validator: Draft202012Validator,
):
    fixture = _load_json(fixture_path)
    errors = sorted(game_state_validator.iter_errors(fixture["initial_state"]), key=str)
    assert errors == [], "\n".join(
        f"{fixture_path}: initial_state: "
        f"{'/'.join(map(str, error.path)) or '<root>'}: {error.message}"
        for error in errors
    )


@pytest.mark.parametrize("fixture_path", FIXTURE_PATHS, ids=lambda path: path.stem)
def test_fixture_id_matches_relative_path(fixture_path: Path):
    fixture = _load_json(fixture_path)
    expected_id = fixture_path.relative_to(FIXTURES_DIR).with_suffix("").as_posix()
    assert fixture["id"] == expected_id


@pytest.mark.parametrize("fixture_path", FIXTURE_PATHS, ids=lambda path: path.stem)
def test_fixture_ruleset_is_current(fixture_path: Path):
    fixture = _load_json(fixture_path)
    assert fixture["ruleset"] == "truco-2p-v1"


@pytest.mark.parametrize("fixture_path", FIXTURE_PATHS, ids=lambda path: path.stem)
def test_fixture_format_is_current(fixture_path: Path):
    fixture = _load_json(fixture_path)
    assert fixture["fixture_version"] == "engine-fixture/v1"


@pytest.mark.parametrize("fixture_path", FIXTURE_PATHS, ids=lambda path: path.stem)
def test_fixture_directory_is_known_aspect(fixture_path: Path):
    fixture = _load_json(fixture_path)
    known_aspects = {
        path.stem
        for path in (SPECS_DIR / "aspects").glob("*.md")
        if path.stem != "TEMPLATE"
    }
    assert fixture["id"].split("/", 1)[0] in known_aspects


@pytest.mark.parametrize("fixture_path", FIXTURE_PATHS, ids=lambda path: path.stem)
def test_steps_present_only_for_valid_state_fixtures(fixture_path: Path):
    fixture = _load_json(fixture_path)
    has_steps = "steps" in fixture
    has_initial_state_error = "expect_initial_state_error" in fixture
    assert has_steps != has_initial_state_error


@pytest.mark.parametrize("fixture_path", FIXTURE_PATHS, ids=lambda path: path.stem)
def test_assert_state_fragments_match_public_state_schema(
    fixture_path: Path,
    partial_public_state_validator: Draft202012Validator,
):
    fixture = _load_json(fixture_path)
    for step in fixture.get("steps", []):
        if step["op"] != "assert_state":
            continue
        errors = sorted(
            partial_public_state_validator.iter_errors(step["expect"]), key=str
        )
        assert errors == [], "\n".join(
            (
                f"{fixture_path}: assert_state: "
                f"{'/'.join(map(str, error.path)) or '<root>'}: {error.message}"
            )
            for error in errors
        )


@pytest.mark.parametrize("fixture_path", FIXTURE_PATHS, ids=lambda path: path.stem)
def test_complete_assertions_match_full_public_state_schema(
    fixture_path: Path,
    public_state_schema: dict,
    public_state_validator: Draft202012Validator,
):
    fixture = _load_json(fixture_path)
    required_fields = set(public_state_schema["required"])
    for step in fixture.get("steps", []):
        if step["op"] != "assert_state":
            continue
        expected = step["expect"]
        if set(expected) != required_fields:
            continue
        errors = sorted(public_state_validator.iter_errors(expected), key=str)
        assert errors == [], "\n".join(
            (
                f"{fixture_path}: complete assert_state: "
                f"{'/'.join(map(str, error.path)) or '<root>'}: {error.message}"
            )
            for error in errors
        )


@pytest.mark.parametrize("fixture_path", FIXTURE_PATHS, ids=lambda path: path.stem)
def test_card_ids_are_unique_within_initial_state(fixture_path: Path):
    fixture = _load_json(fixture_path)
    seen_card_ids: set[str] = set()
    for cards in fixture["initial_state"]["hands"].values():
        for card in cards:
            card_id = card["id"]
            assert card_id not in seen_card_ids
            seen_card_ids.add(card_id)


@pytest.mark.parametrize("fixture_path", FIXTURE_PATHS, ids=lambda path: path.stem)
def test_actions_reference_existing_card_ids(fixture_path: Path):
    fixture = _load_json(fixture_path)
    known_card_ids = {
        card["id"]
        for cards in fixture["initial_state"]["hands"].values()
        for card in cards
    }
    for step in fixture.get("steps", []):
        actions = []
        if step["op"] in {"apply_action", "assert_rejected_action"}:
            actions.append(step["action"])
        elif step["op"] == "assert_legal_actions":
            actions.extend(step.get("must_include", []))
            actions.extend(step.get("must_exclude", []))
        for action in actions:
            card_id = action.get("card_id")
            if card_id is not None:
                assert card_id in known_card_ids
