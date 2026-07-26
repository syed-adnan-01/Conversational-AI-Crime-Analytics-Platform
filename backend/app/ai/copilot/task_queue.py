"""
Task Queue for async copilot background tasks.
"""

import threading
from collections import deque
from datetime import datetime
from typing import Deque, Dict, Optional

from app.ai.copilot.copilot_models import CopilotTask, TaskStatus


class TaskQueue:
    """Thread-safe in-memory task queue."""

    def __init__(self) -> None:
        self._queue: Deque[CopilotTask] = deque()
        self._store: Dict[str, CopilotTask] = {}
        self._lock = threading.Lock()

    def enqueue(self, task: CopilotTask) -> CopilotTask:
        with self._lock:
            self._queue.append(task)
            self._store[task.task_id] = task
        return task

    def dequeue(self) -> Optional[CopilotTask]:
        with self._lock:
            if self._queue:
                task = self._queue.popleft()
                task.status = TaskStatus.RUNNING
                self._store[task.task_id] = task
                return task
        return None

    def mark_done(self, task_id: str, result: dict) -> None:
        with self._lock:
            if task_id in self._store:
                self._store[task_id].status = TaskStatus.DONE
                self._store[task_id].result = result
                self._store[task_id].completed_at = datetime.utcnow()

    def mark_failed(self, task_id: str, error: str) -> None:
        with self._lock:
            if task_id in self._store:
                self._store[task_id].status = TaskStatus.FAILED
                self._store[task_id].error = error
                self._store[task_id].completed_at = datetime.utcnow()

    def get(self, task_id: str) -> Optional[CopilotTask]:
        return self._store.get(task_id)

    def size(self) -> int:
        return len(self._queue)
