"""Build reproducible release artifacts for the public Truco specification."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import re
import tarfile
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RELEASE_PATHS = (
    Path("LICENSE"),
    Path("README.md"),
    Path("VERSION"),
    Path("spec-manifest.json"),
    Path("rulesets"),
    Path("engine"),
    Path("exploration"),
    Path("notation"),
    Path("schemas"),
)
MANIFESTED_PATHS = frozenset(
    {"VERSION", "rulesets", "engine", "exploration", "notation", "schemas"}
)
VERSION_PATTERN = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?$")
RELEASE_FORMAT = "truco-spec-release/v1"
NORMALIZED_MTIME = 0
FILE_MODE = 0o644
DIRECTORY_MODE = 0o755


def _sha256(contents: bytes) -> str:
    return hashlib.sha256(contents).hexdigest()


def _release_entries(root: Path) -> list[tuple[Path, bool]]:
    entries: list[tuple[Path, bool]] = []
    for relative_path in RELEASE_PATHS:
        path = root / relative_path
        if path.is_symlink():
            raise ValueError(f"release path may not be a symlink: {relative_path}")
        if path.is_file():
            entries.append((relative_path, False))
            continue
        if not path.is_dir():
            raise FileNotFoundError(relative_path)

        entries.append((relative_path, True))
        for candidate in path.rglob("*"):
            candidate_relative = candidate.relative_to(root)
            if candidate.is_symlink():
                raise ValueError(
                    f"release path may not be a symlink: {candidate_relative}"
                )
            if candidate.is_dir():
                entries.append((candidate_relative, True))
            elif candidate.is_file():
                entries.append((candidate_relative, False))
            else:
                raise ValueError(
                    f"release path must be a regular file or directory: "
                    f"{candidate_relative}"
                )

    return sorted(entries, key=lambda entry: entry[0].as_posix())


def _load_spec_manifest(root: Path) -> dict[str, Any]:
    manifest_path = root / "spec-manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError("spec-manifest.json is not valid JSON") from error

    if manifest.get("format") != "truco-spec-manifest/v1":
        raise ValueError("spec-manifest.json has an unsupported format")
    version = manifest.get("version")
    if not isinstance(version, str) or VERSION_PATTERN.fullmatch(version) is None:
        raise ValueError("spec-manifest.json has an invalid version")
    return manifest


def _verify_manifest_files(
    root: Path,
    entries: list[tuple[Path, bool]],
    manifest: dict[str, Any],
) -> list[dict[str, Any]]:
    payload_files = {
        path.as_posix(): root.joinpath(path).read_bytes()
        for path, is_directory in entries
        if not is_directory and path.parts[0] in MANIFESTED_PATHS
    }

    manifest_files: dict[str, dict[str, Any]] = {}
    for entry in manifest.get("files", []):
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise ValueError("spec-manifest.json has an invalid files entry")
        path = entry["path"]
        manifest_path = PurePosixPath(path)
        if (
            manifest_path.is_absolute()
            or ".." in manifest_path.parts
            or not manifest_path.parts
        ):
            raise ValueError(f"spec-manifest.json has an unsafe file path: {path}")
        if path in manifest_files:
            raise ValueError(f"spec-manifest.json repeats a file: {path}")
        manifest_files[path] = entry

    if payload_files.keys() != manifest_files.keys():
        missing = sorted(manifest_files.keys() - payload_files.keys())
        unexpected = sorted(payload_files.keys() - manifest_files.keys())
        details = []
        if missing:
            details.append(f"missing {missing!r}")
        if unexpected:
            details.append(f"unexpected {unexpected!r}")
        raise ValueError(
            "release payload files do not match spec-manifest.json: "
            + "; ".join(details)
        )

    inventory = []
    for path, contents in sorted(payload_files.items()):
        expected = manifest_files[path]
        digest = _sha256(contents)
        if expected.get("bytes") != len(contents) or expected.get("sha256") != digest:
            raise ValueError(f"release payload file is stale in manifest: {path}")
        inventory.append({"path": path, "bytes": len(contents), "sha256": digest})

    schema_reference = manifest.get("$schema")
    if not isinstance(schema_reference, str) or not schema_reference.startswith("./"):
        raise ValueError("spec-manifest.json has an invalid $schema reference")
    schema_path = PurePosixPath(schema_reference.removeprefix("./"))
    if (
        schema_path.is_absolute()
        or ".." in schema_path.parts
        or schema_path.as_posix() not in manifest_files
    ):
        raise ValueError(
            "spec-manifest.json $schema target is not in the release payload"
        )
    return inventory


def _tar_info(name: str, *, is_directory: bool, size: int = 0) -> tarfile.TarInfo:
    info = tarfile.TarInfo(name)
    info.type = tarfile.DIRTYPE if is_directory else tarfile.REGTYPE
    info.size = 0 if is_directory else size
    info.mode = DIRECTORY_MODE if is_directory else FILE_MODE
    info.uid = 0
    info.gid = 0
    info.uname = "root"
    info.gname = "root"
    info.mtime = NORMALIZED_MTIME
    info.pax_headers = {}
    return info


def _render_archive(
    root: Path,
    entries: list[tuple[Path, bool]],
    archive_root: str,
) -> bytes:
    output = io.BytesIO()
    with gzip.GzipFile(
        filename="",
        mode="wb",
        compresslevel=9,
        fileobj=output,
        mtime=NORMALIZED_MTIME,
    ) as compressed:
        with tarfile.open(
            fileobj=compressed,
            mode="w",
            format=tarfile.PAX_FORMAT,
        ) as archive:
            archive.addfile(_tar_info(archive_root, is_directory=True))
            for relative_path, is_directory in entries:
                member_name = f"{archive_root}/{relative_path.as_posix()}"
                if is_directory:
                    archive.addfile(_tar_info(member_name, is_directory=True))
                    continue

                contents = (root / relative_path).read_bytes()
                archive.addfile(
                    _tar_info(member_name, is_directory=False, size=len(contents)),
                    io.BytesIO(contents),
                )
    return output.getvalue()


def _write_atomically(path: Path, contents: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as temporary_file:
            temporary_file.write(contents)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        temporary_path.replace(path)
    except BaseException:
        temporary_path.unlink(missing_ok=True)
        raise


def build_release(
    root: Path = ROOT,
    output_dir: Path | None = None,
) -> dict[str, Path]:
    """Build the archive, release inventory, and checksum file."""

    root = root.resolve()
    output_dir = (output_dir or root / "dist").resolve()
    entries = _release_entries(root)
    manifest = _load_spec_manifest(root)
    inventory = _verify_manifest_files(root, entries, manifest)
    version = manifest["version"]
    archive_root = f"truco-spec-{version}"
    archive_name = f"{archive_root}.tar.gz"
    release_manifest_name = f"{archive_root}.release.json"

    archive_contents = _render_archive(root, entries, archive_root)
    archive_digest = _sha256(archive_contents)
    release_manifest = {
        "archive": {
            "bytes": len(archive_contents),
            "file": archive_name,
            "sha256": archive_digest,
        },
        "contents": inventory,
        "format": RELEASE_FORMAT,
        "normalized_mtime": NORMALIZED_MTIME,
        "root": archive_root,
        "version": version,
    }
    release_manifest_contents = (
        json.dumps(release_manifest, indent=2, sort_keys=True) + "\n"
    ).encode()

    checksums = {
        archive_name: archive_digest,
        release_manifest_name: _sha256(release_manifest_contents),
    }
    checksum_contents = "".join(
        f"{digest}  {name}\n" for name, digest in sorted(checksums.items())
    ).encode()

    artifacts = {
        "archive": output_dir / archive_name,
        "release_manifest": output_dir / release_manifest_name,
        "checksums": output_dir / "SHA256SUMS",
    }
    _write_atomically(artifacts["archive"], archive_contents)
    _write_atomically(artifacts["release_manifest"], release_manifest_contents)
    _write_atomically(artifacts["checksums"], checksum_contents)
    return artifacts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "dist",
        help="directory for release artifacts (default: dist)",
    )
    args = parser.parse_args()
    artifacts = build_release(output_dir=args.output_dir)
    for path in artifacts.values():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
