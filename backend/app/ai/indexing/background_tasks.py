"""
============================================================
Background Indexing Tasks
============================================================

Module  : AI Indexing Subsystem
Purpose : Asynchronous worker task hooks for background index execution.
"""

from app.core.logging import app_logger


def run_background_indexing(case_id: str, force: bool = False) -> None:
    """
    Background task hook suitable for FastAPI BackgroundTasks, Celery, or Kafka workers.
    Executes case indexing asynchronously without blocking API responses.
    """
    from app.ai.indexing.index_manager import IndexManager

    app_logger.info("Starting background indexing for case | CaseID=%s | Force=%s", case_id, force)
    try:
        manager = IndexManager()
        result = manager.index_case(case_id=case_id, force=force)
        app_logger.info("Background indexing completed | CaseID=%s | Status=%s | Chunks=%s", case_id, result.status, result.chunk_count)
    except Exception as exc:
        app_logger.error("Background indexing failed | CaseID=%s | Error=%s", case_id, exc)
