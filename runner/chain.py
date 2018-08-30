from time import sleep


def run_chain(run_spec, message):
    message("Working!")
    sleep(5)
    message("Done!")
    return True
