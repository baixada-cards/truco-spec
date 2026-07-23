"""Validation for reproducible public release artifacts."""

from __future__ import annotations

import hashlib
import json
import tarfile
from pathlib import Path

import pytest

from scripts.build_release import (
    DIRECTORY_MODE,
    FILE_MODE,
    NORMALIZED_MTIME,
    build_release,
)


def _sha256(contents: bytes) -> str:
    return hashlib.sha256(contents).hexdigest()


def _write_release_source(root: Path) -> None:
    files = {
        "LICENSE": b"Example license\n",
        "README.md": b"# Example specification\n",
        "VERSION": b"1.2.3-rc.1\n",
        "rulesets/truco-2p-v1.md": b"# Rules\n",
        "engine/fixtures/example.json": b'{"fixture_version":"engine-fixture/v1"}\n',
        "exploration/CONTRACT.md": b"# Exploration\n",
        "notation/schemas/fixture.schema.json": b'{"type":"object"}\n',
        "schemas/spec-manifest.schema.json": b'{"type":"object"}\n',
    }
    for relative_path, contents in files.items():
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(contents)

    payload_files = [
        {
            "bytes": len(contents),
            "path": relative_path,
            "sha256": _sha256(contents),
        }
        for relative_path, contents in sorted(files.items())
        if relative_path.split("/", maxsplit=1)[0]
        in {"VERSION", "rulesets", "engine", "exploration", "notation", "schemas"}
    ]
    manifest = {
        "$schema": "./schemas/spec-manifest.schema.json",
        "files": payload_files,
        "format": "truco-spec-manifest/v1",
        "version": "1.2.3-rc.1",
    }
    (root / "spec-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _artifact_bytes(artifacts: dict[str, Path]) -> dict[str, bytes]:
    return {path.name: path.read_bytes() for path in artifacts.values()}


def test_release_is_byte_identical_and_metadata_is_normalized(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    _write_release_source(source)

    first = build_release(source, tmp_path / "first")
    second = build_release(source, tmp_path / "second")

    assert _artifact_bytes(first) == _artifact_bytes(second)
    archive_contents = first["archive"].read_bytes()
    assert archive_contents[4:8] == NORMALIZED_MTIME.to_bytes(4, "little")

    with tarfile.open(first["archive"], mode="r:gz") as archive:
        members = archive.getmembers()
        names = [member.name for member in members]
        assert names == [
            "truco-spec-1.2.3-rc.1",
            "truco-spec-1.2.3-rc.1/LICENSE",
            "truco-spec-1.2.3-rc.1/README.md",
            "truco-spec-1.2.3-rc.1/VERSION",
            "truco-spec-1.2.3-rc.1/engine",
            "truco-spec-1.2.3-rc.1/engine/fixtures",
            "truco-spec-1.2.3-rc.1/engine/fixtures/example.json",
            "truco-spec-1.2.3-rc.1/exploration",
            "truco-spec-1.2.3-rc.1/exploration/CONTRACT.md",
            "truco-spec-1.2.3-rc.1/notation",
            "truco-spec-1.2.3-rc.1/notation/schemas",
            "truco-spec-1.2.3-rc.1/notation/schemas/fixture.schema.json",
            "truco-spec-1.2.3-rc.1/rulesets",
            "truco-spec-1.2.3-rc.1/rulesets/truco-2p-v1.md",
            "truco-spec-1.2.3-rc.1/schemas",
            "truco-spec-1.2.3-rc.1/schemas/spec-manifest.schema.json",
            "truco-spec-1.2.3-rc.1/spec-manifest.json",
        ]
        assert names == sorted(names)

        for member in members:
            assert member.uid == 0
            assert member.gid == 0
            assert member.uname == "root"
            assert member.gname == "root"
            assert member.mtime == NORMALIZED_MTIME
            assert member.mode == (DIRECTORY_MODE if member.isdir() else FILE_MODE)

        archive_root = "truco-spec-1.2.3-rc.1"
        embedded_manifest = json.loads(
            archive.extractfile(f"{archive_root}/spec-manifest.json").read()
        )
        for entry in embedded_manifest["files"]:
            contents = archive.extractfile(f"{archive_root}/{entry['path']}").read()
            assert entry["bytes"] == len(contents)
            assert entry["sha256"] == _sha256(contents)
        schema_path = embedded_manifest["$schema"].removeprefix("./")
        assert archive.getmember(f"{archive_root}/{schema_path}").isfile()

    release_manifest = json.loads(first["release_manifest"].read_text())
    assert release_manifest["format"] == "truco-spec-release/v1"
    assert release_manifest["version"] == "1.2.3-rc.1"
    assert release_manifest["archive"] == {
        "bytes": len(archive_contents),
        "file": first["archive"].name,
        "sha256": _sha256(archive_contents),
    }

    checksum_lines = first["checksums"].read_text().splitlines()
    assert checksum_lines == sorted(
        checksum_lines, key=lambda line: line.split("  ")[1]
    )
    for line in checksum_lines:
        digest, name = line.split("  ")
        assert digest == _sha256((first["checksums"].parent / name).read_bytes())


def test_release_rejects_contract_file_missing_from_manifest(tmp_path: Path) -> None:
    source = tmp_path / "source"
    _write_release_source(source)
    (source / "engine" / "untracked.json").write_text("{}\n", encoding="utf-8")

    with pytest.raises(ValueError, match="do not match spec-manifest.json"):
        build_release(source, tmp_path / "dist")


def test_release_rejects_schema_target_outside_manifest(tmp_path: Path) -> None:
    source = tmp_path / "source"
    _write_release_source(source)
    manifest_path = source / "spec-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["$schema"] = "./schemas/missing.schema.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match=r"\$schema target is not"):
        build_release(source, tmp_path / "dist")


def test_release_rejects_symlinks(tmp_path: Path) -> None:
    source = tmp_path / "source"
    _write_release_source(source)
    (source / "engine" / "linked.json").symlink_to(
        source / "engine" / "fixtures" / "example.json"
    )

    with pytest.raises(ValueError, match="may not be a symlink"):
        build_release(source, tmp_path / "dist")
