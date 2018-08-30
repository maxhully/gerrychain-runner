import pytest
from unittest.mock import MagicMock
from runner.queue import Queue


@pytest.fixture
def queue():
    Redis = MagicMock()
    Task = MagicMock()
    return Queue(dict(), key="queue", Cache=Redis, Task=Task)


def test_queue_sets_status_to_RUNNING_when_getting_new_task(queue):
    queue.update_status = MagicMock()

    queue.redis.brpop.return_value = ("queue", '{"id": "mock-id"}')
    queue.get_next_task()

    assert queue.update_status.call_args[0] == (queue, "mock-id", "RUNNING")


def test_queue_only_accepts_statuses_among_WAITING_FAILED_RUNNING_and_COMPLETE(queue):
    for status in ("WAITING", "FAILED", "RUNNING", "COMPLETE"):
        queue.update_status("mock-task-key", status)

    with pytest.raises(ValueError):
        queue.update_status("mock-task-key", "invalid status")
