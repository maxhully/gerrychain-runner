import json
import networkx
from rundmcmc.partition import GeographicPartition

from rundmcmc.updaters import DataTally, Election


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
