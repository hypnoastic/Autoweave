"""Bootstrap helpers for the AutoWeave repository layout."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from autoweave.templates import sample_project

DOC_FILES = (
    Path("docs/autoweave_high_level_architecture.md"),
    Path("docs/autoweave_implementation_spec.md"),
    Path("docs/autoweave_diagrams_source.md"),
)

AGENT_ROLES = sample_project.AGENT_ROLES
AGENT_FILES = sample_project.AGENT_FILES
RUNTIME_FILES = sample_project.RUNTIME_FILES
WORKFLOW_FILE = sample_project.WORKFLOW_FILE
ROUTING_FILE = sample_project.ROUTING_FILE
TEMPLATE_PROJECT_FILES = tuple(sample_project.render_project_files().keys())


@dataclass(frozen=True)
class BootstrapResult:
    created: tuple[Path, ...]
    updated: tuple[Path, ...] = ()


@dataclass(frozen=True)
class MigrationResult:
    created: tuple[Path, ...]
    updated: tuple[Path, ...]
    unchanged: tuple[Path, ...] = ()


def repository_root(root: Path | None = None) -> Path:
    return (Path.cwd() if root is None else root).resolve()


def expected_repository_files(root: Path) -> tuple[Path, ...]:
    return tuple(root / relative for relative in (*DOC_FILES, *TEMPLATE_PROJECT_FILES))


def bootstrap_repository(root: Path, *, overwrite: bool = False) -> BootstrapResult:
    created: list[Path] = []
    updated: list[Path] = []

    for role in AGENT_ROLES:
        role_created, role_updated = _write_agent_bundle(root, name=role, role=role, overwrite=overwrite)
        created.extend(role_created)
        updated.extend(role_updated)

    bundle_created, bundle_updated = _write_text_file(
        root / WORKFLOW_FILE,
        sample_project.render_workflow_yaml(),
        overwrite=overwrite,
    )
    created.extend(bundle_created)
    updated.extend(bundle_updated)
    bundle_created, bundle_updated = _write_text_file(
        root / ROUTING_FILE,
        sample_project.render_model_profiles_yaml(),
        overwrite=overwrite,
    )
    created.extend(bundle_created)
    updated.extend(bundle_updated)
    for path, content in sample_project.render_runtime_files().items():
        bundle_created, bundle_updated = _write_text_file(root / path, content, overwrite=overwrite)
        created.extend(bundle_created)
        updated.extend(bundle_updated)

    return BootstrapResult(created=tuple(created), updated=tuple(updated))


def create_agent(root: Path, name: str, role: str | None = None, *, overwrite: bool = False) -> BootstrapResult:
    agent_role = role or name
    created, updated = _write_agent_bundle(root, name=name, role=agent_role, overwrite=overwrite)
    return BootstrapResult(created=tuple(created), updated=tuple(updated))


def migrate_repository(root: Path, *, dry_run: bool = False) -> MigrationResult:
    created: list[Path] = []
    updated: list[Path] = []
    unchanged: list[Path] = []
    for relative_path, content in sample_project.render_project_files().items():
        absolute_path = root / relative_path
        status = _sync_text_file(absolute_path, content, dry_run=dry_run)
        if status == "created":
            created.append(absolute_path)
        elif status == "updated":
            updated.append(absolute_path)
        else:
            unchanged.append(absolute_path)
    return MigrationResult(created=tuple(created), updated=tuple(updated), unchanged=tuple(unchanged))


def _write_agent_bundle(root: Path, name: str, role: str, *, overwrite: bool) -> tuple[list[Path], list[Path]]:
    agent_dir = root / "agents" / name
    files = {
        agent_dir / "soul.md": sample_project.render_agent_soul(role),
        agent_dir / "playbook.yaml": sample_project.render_agent_playbook(role),
        agent_dir / "autoweave.yaml": sample_project.render_agent_autoweave(role),
    }
    for relative_path, content in sample_project.render_agent_skill_files(role).items():
        files[agent_dir / relative_path] = content
    created: list[Path] = []
    updated: list[Path] = []
    for path, content in files.items():
        file_created, file_updated = _write_text_file(path, content, overwrite=overwrite)
        created.extend(file_created)
        updated.extend(file_updated)
    return created, updated


def _write_text_file(path: Path, content: str, *, overwrite: bool) -> tuple[list[Path], list[Path]]:
    if path.exists() and not overwrite:
        return [], []
    path.parent.mkdir(parents=True, exist_ok=True)
    existed = path.exists()
    path.write_text(content, encoding="utf-8")
    if existed:
        return [], [path]
    return [path], []


def _sync_text_file(path: Path, content: str, *, dry_run: bool) -> str:
    if not path.exists():
        if not dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        return "created"

    existing = path.read_text(encoding="utf-8")
    if existing == content:
        return "unchanged"

    if not dry_run:
        path.write_text(content, encoding="utf-8")
    return "updated"
