"""Public project bootstrap helpers for installed AutoWeave consumers."""

from __future__ import annotations

from pathlib import Path


def bootstrap_project(root: str | Path, *, overwrite: bool = False):
    from apps.cli.bootstrap import bootstrap_repository

    return bootstrap_repository(Path(root).resolve(), overwrite=overwrite)


def migrate_project(root: str | Path, *, dry_run: bool = False):
    from apps.cli.bootstrap import migrate_repository

    return migrate_repository(Path(root).resolve(), dry_run=dry_run)
