class ChainConfig:
    def __init__(self, task_spec):
        pass


def run_chain(task, update_status):
    update_status("Initializing...")
    chain_config = ChainConfig(task)

    chain = chain_config.chain
    reports = chain_config.reports

    for state in chain:
        for report in reports:
            report(state)

    raise NotImplementedError
