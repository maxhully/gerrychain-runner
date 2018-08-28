from rundmcmc.output import SlimPValueReport, Histogram
from rundmcmc.updaters import Election


class Report:
    def __init__(self, partition):
        elections = [
            updater for updater in partition.updaters if isinstance(updater, Election)
        ]
        self.p_value_reports = [SlimPValueReport(election) for election in elections]
        self.histograms = []
