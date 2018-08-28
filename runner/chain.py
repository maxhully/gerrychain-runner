import json

from rundmcmc.defaults import DefaultChain
from rundmcmc.partition import GeographicPartition
from rundmcmc.updaters import DataTally, Election

from .partition import resolve_partition


def run_chain(run, set_message):
    set_message("Initializing...")

    chain = configure_chain(run)

    for state in chain:
        print(state)

    raise NotImplementedError


def configure_chain(run):
    partition = resolve_partition(run)
    constraints = resolve_constraints(run.constraints)
    total_steps = run.total_steps

    chain = DefaultChain(partition, constraints, total_steps)
    return chain


def resolve_constraints(constraints):
    pass


def resolve_run(run):
    graph = get_graph()

    assignment = {node: graph.nodes[node]["ASM"] for node in graph.nodes}

    elections = [
        Election("2016 Presidential", ["PREDEM16_n", "PREREP16_n"]),
        Election("2012 Presidential", ["PREDEM12_n", "PREREP12_n"]),
        Election("2016 US Senate", ["USSDEM16_n", "USSREP12_n"]),
        Election("2012 US Senate", ["USSDEM12_n", "USSREP12_n"]),
        Election("2014 Governor", ["GOVDEM14_n", "GOVREP14_n"]),
        Election("2012 Governor (Recall)", ["GOVDEM12_n", "GOVREP12_n"]),
    ]

    updaters = {"population": DataTally("PERSONS", alias="population")}

    for election in elections:
        updaters[election.name] = election

    partition = GeographicPartition(graph, assignment, updaters)

    return partition


def get_graph():
    with open("/data/wisconsin_graph.json") as f:
        data = json.load(f)
    return networkx.readwrite.json_graph.adjacency_graph(data)
