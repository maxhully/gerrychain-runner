from unittest.mock import MagicMock, patch

import pytest

from runner.__main__ import get_task_and_run


@pytest.fixture
def queue():
    queue = MagicMock()
    mock_run = MagicMock()
    mock_run.id = "1234"
    queue.get_next_task.return_value = mock_run
    return queue


def test_get_task_and_run_gets_task_from_queue(queue):
    with patch("runner.chain"):
        get_task_and_run(queue)
    assert queue.get_next_task.call_count == 1


def test_runner_returns_failed_tasks_to_queue(queue):
    with patch("runner.__main__.run_chain") as run_chain:
        run_chain.side_effect = Exception("Mock exception")
        get_task_and_run(queue)
    assert queue.return_failed_task.call_count == 1


def test_runner_sets_status_to_complete_when_done(queue):
    with patch("runner.chain"):
        get_task_and_run(queue)
    assert queue.complete_task.call_count == 1
