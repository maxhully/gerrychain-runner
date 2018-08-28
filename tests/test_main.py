from unittest.mock import MagicMock, patch

import pytest

from runner.__main__ import get_task_and_run


@pytest.fixture
def queue():
    queue = MagicMock()
    mock_run = MagicMock()
    mock_run.id = "1234"
    queue.get_next_task.return_value = mock_run


@patch("runner.chain")
def test_get_task_and_run_gets_task_from_queue(queue, mock_chain):
    get_task_and_run(queue)

    assert queue.get_next_task.call_count == 1


@patch("runner.chain")
def test_runner_returns_failed_tasks_to_queue(queue, mock_chain):
    run_chain = mock_chain.run_chain
    run_chain.side_effect = Exception

    get_task_and_run(queue)

    assert queue.return_failed_task.call_count == 1
