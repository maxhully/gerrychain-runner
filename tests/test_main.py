from unittest.mock import MagicMock, patch

from runner.__main__ import get_task_and_run


@patch("runner.__main__.run_chain")
def test_get_task_and_run_gets_task_from_queue():
    queue = MagicMock()
    queue.get_next_task.return_value = {"id": "1234"}

    get_task_and_run(queue)

    assert queue.get_next_task.call_count > 0
