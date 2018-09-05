import json

import networkx


class Graph(networkx.Graph):
    @classmethod
    def from_json(cls, f):
        data = json.load(f)
        graph = networkx.readwrite.json_graph.adjacency_graph(data)
        # graph = networkx.relabel.convert_node_labels_to_integers(graph)
        return cls(graph)

    def to_json(self, f):
        data = networkx.readwrite.json_graph.adjacency_data(self)
        json.dump(data, f)

    def assert_has_fields(self, required_fields):
        for node, data in self.nodes.data():
            for field in required_fields:
                if field not in data:
                    raise AssertionError(
                        "The nodes are missing some required properties."
                        "{} is missing {}".format(node, field)
                    )

    def assignment_from_attribute(self, attribute):
        return {node: self.nodes[node][attribute] for node in self.nodes}

    @classmethod
    def from_shapefile(cls, filepath):
        raise NotImplemented

    def validate_geography(self):
        suspiciously_small_nodes = [
            node for node in self.nodes if self.nodes[node]["areas"] < 1
        ]
        percent_suspicious_nodes = len(suspiciously_small_nodes) / len(self.nodes)
        if percent_suspicious_nodes > 0.01:
            raise AssertionError(
                "Too many nodes ({}%) have area < 1".format(
                    round(percent_suspicious_nodes * 100, 2)
                )
            )

        suspiciously_small_edges = [
            edge for edge in self.edges if self.edges[edge]["shared_perim"] < 1
        ]
        percent_suspicious_edges = len(suspiciously_small_edges) / len(self.edges)

        if percent_suspicious_edges > 0.01:
            raise AssertionError(
                "Too many edges ({}%) have shared_perim < 1".format(
                    round(percent_suspicious_edges * 100, 2)
                )
            )

        return True


def main():
    with open("./PA_FINAL_Full.json") as f:
        graph = Graph.from_json(f)
    if graph.validate_geography():
        print("Geography is valid!")


if __name__ == "__main__":
    main()
