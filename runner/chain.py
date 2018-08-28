from time import sleep


def run_chain(run_spec, update_status):
    update_status("Working!")
    sleep(5)
    return True
