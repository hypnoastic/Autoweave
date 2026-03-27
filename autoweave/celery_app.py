"""Module-level Celery app for external worker entrypoints."""

from __future__ import annotations

from autoweave.celery_queue import celery_app

__all__ = ["celery_app"]
