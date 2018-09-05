import random
import sys


from rundmcmc.accept import always_accept
from rundmcmc.chain import MarkovChain
from rundmcmc.output.output import SlimPValueReport
from rundmcmc.partition import Partition
from rundmcmc.proposals import propose_random_flip
from rundmcmc.updaters import (
    Tally,
    boundary_nodes,
    county_splits,
    cut_edges,
    cut_edges_by_part,
    exterior_boundaries,
    interior_boundaries,
    perimeters,
    polsby_popper,
)
from rundmcmc.updaters.election import Election
from rundmcmc.validity import (
    L_minus_1_polsby_popper,
    LowerBound,
    Validator,
    refuse_new_splits,
    single_flip_contiguous,
    within_percent_of_ideal_population,
)

from graph import Graph


def get_elections(election_names, election_columns):
    elections = [
        Election(name, {"Republican": cols[1], "Democratic": cols[0]})
        for name, cols in zip(election_names, election_columns)
    ]
    return elections


def get_updaters():
    # Names of graph columns go here
    pop_col = "P0050001"
    county_col = "COUNTYFP10"

    updaters = {
        "perimeters": perimeters,
        "exterior_boundaries": exterior_boundaries,
        "interior_boundaries": interior_boundaries,
        "boundary_nodes": boundary_nodes,
        "cut_edges": cut_edges,
        "cut_edges_by_part": cut_edges_by_part,
        "polsby_popper": polsby_popper,
        "areas": Tally("areas"),
        "population": Tally(pop_col, alias="population"),
        "County_Splits": county_splits("County_Splits", county_col),
    }

    election_names = (
        "Governor_2010",
        "Senate_2010",
        "AttorneyGeneral_2012",
        "President_2012",
        "Senate_2012",
        "Governor_2014",
        "AttorneyGeneral_2016",
        "Presdent_2016",
        "Senate_2016",
        "SenW",
    )
    election_columns = (
        ("GOV10D", "GOV10R"),
        ("SEN10D", "SEN10R"),
        ("ATG12D", "ATG12R"),
        ("PRES12D", "PRES12R"),
        ("USS12D", "USS12R"),
        ("F2014GovD", "F2014GovR"),
        ("T16ATGD", "T16ATGR"),
        ("T16PRESD", "T16PRESR"),
        ("T16SEND", "T16SENR"),
        ("SenWD", "SenWR"),
    )

    elections = get_elections(election_names, election_columns)

    updaters.update({election.name: election for election in elections})

    required_fields = [pop_col, county_col] + [
        col for pair in election_columns for col in pair
    ]

    return updaters, required_fields


def get_partition(plan, graph_path="./PA_FINAL_Full.json"):
    with open(graph_path) as f:
        graph = Graph.from_json(f)
    updaters, required_fields = get_updaters()
    graph.assert_has_fields(required_fields)
    assignment = graph.assignment_from_attribute(plan)
    return Partition(graph=graph, assignment=assignment, updaters=updaters)


def get_constraints(partition):
    pop_limit = .01
    population_constraint = within_percent_of_ideal_population(partition, pop_limit)

    compactness_constraint_Lm1 = LowerBound(
        L_minus_1_polsby_popper, L_minus_1_polsby_popper(partition) - 0.01
    )

    county_constraint = refuse_new_splits("County_Splits")

    return [
        single_flip_contiguous,
        population_constraint,
        compactness_constraint_Lm1,
        county_constraint,
    ]


def get_chain(plan, steps):
    initial_partition = get_partition(plan)
    constraints = get_constraints(initial_partition)

    chain = MarkovChain(
        propose_random_flip,
        Validator(constraints),
        always_accept,
        initial_partition,
        total_steps=steps,
    )

    return chain


def run_chain(length, seed=1965, plan="Remedial_p", callback=print):
    random.seed(seed)

    chain = get_chain(plan, steps=length)

    reports = {
        name: SlimPValueReport(election)
        for name, election in chain.state.updaters.items()
        if isinstance(election, Election)
    }

    interval = max(round(length / 100), 1)

    for i, step in enumerate(chain):
        if i % interval == 0:
            callback("Step {}".format(i))
        for name, report in reports.items():
            report(step)
    return [report.render() for report in reports.values()]


def combine(first_reports, second_reports):
    reports = {report["election"]: report["analysis"] for report in first_reports}

    for name, report in reports.items():
        for score, counter in report.counters:
            counter.update(second_reports[name].counters[score])
    return reports


def main():
    pass


if __name__ == "__main__":
    args = sys.argv[1:]
    length = int(args[0])

    if len(args) > 1:
        output_file = args[1]
    else:
        output_file = "./report.json"

    main(length, output_file)
