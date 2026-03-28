from pathlib import Path

from autoweave import bootstrap_project, migrate_project


def test_cli_entry_import_does_not_hit_public_package_cycle() -> None:
    import apps.cli.main as cli_main

    assert cli_main.main is not None


def test_public_project_helpers_bootstrap_and_migrate(tmp_path: Path) -> None:
    result = bootstrap_project(tmp_path)

    assert result.created
    assert (tmp_path / "configs" / "workflows" / "team.workflow.yaml").exists()

    migration = migrate_project(tmp_path)

    assert migration.created == ()
    assert isinstance(migration.updated, tuple)
