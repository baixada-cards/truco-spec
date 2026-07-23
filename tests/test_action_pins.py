from pathlib import Path

from scripts.check_action_pins import find_unpinned_actions

FULL_SHA = "0123456789abcdef0123456789abcdef01234567"


def _write_workflow(root: Path, body: str) -> Path:
    workflow = root / ".github" / "workflows" / "test.yml"
    workflow.parent.mkdir(parents=True)
    workflow.write_text(body, encoding="utf-8")
    return workflow


def test_accepts_local_actions_and_full_commit_pins(tmp_path: Path) -> None:
    workflows = tmp_path / ".github" / "workflows"
    _write_workflow(
        tmp_path,
        f"""
steps:
  - uses: ./actions/local
  - uses: owner-name/repo.name@{FULL_SHA} # release label
  - uses: owner-name/repo.name/subdirectory@{FULL_SHA}
""",
    )

    assert find_unpinned_actions(workflows) == []


def test_rejects_tags_branches_docker_and_expressions(tmp_path: Path) -> None:
    workflows = tmp_path / ".github" / "workflows"
    workflow = _write_workflow(
        tmp_path,
        """
steps:
  - uses: actions/checkout@v7
  - uses: owner/action@main
  - uses: docker://alpine:3
  - uses: ${{ matrix.action }}
""",
    )

    failures = find_unpinned_actions(workflows)

    assert [
        (failure.path, failure.line_number, failure.reference) for failure in failures
    ] == [
        (workflow, 3, "actions/checkout@v7"),
        (workflow, 4, "owner/action@main"),
        (workflow, 5, "docker://alpine:3"),
        (workflow, 6, "${{ matrix.action }}"),
    ]


def test_repository_workflows_are_fully_pinned() -> None:
    assert find_unpinned_actions() == []
