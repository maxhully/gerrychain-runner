from .split_chain import run_chain


def run(run_spec, message):
    length = run_spec.total_steps
    plan = run_spec.plan
    callback = message

    reports = run_chain(length, plan=plan, callback=callback)
    return reports
