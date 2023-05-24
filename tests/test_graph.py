import os
import unittest

from graph import Graph

from .utils import current_dir

_test_graph1 = os.path.join(current_dir(__file__), "test1_graph.txt")


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.g1 = Graph()
        self.g1.initialize_from_file(_test_graph1)

    def test_vertex_collection(self):
        self.assertEqual(
            sorted(self.g1.vertex_collection),
            ["a", "b", "c", "d", "e", "f"],
            "incorrect vertices",
        )

    def test_edge_collection(self):
        edges = self.g1.edge_collection
        for e in [{"a", "d"}, {"d", "c"}, {"b", "c"}, {"e", "c"}]:
            self.assertIn(e, edges, f"{e} not in graph")

    def test_get_adjacent_vertices(self):
        self.assertEqual(
            self.g1.get_adjacent_vertices("c"),
            ["b", "d", "e"],
        )
        self.assertEqual(
            self.g1.get_adjacent_vertices("x"),
            ["x not in graph"],
        )

    def test_add_vertex(self):
        self.g1.add_vertex("z")
        self.assertEqual(
            sorted(self.g1.vertex_collection),
            ["a", "b", "c", "d", "e", "f", "z"],
        )

    def test_add_edge(self):
        self.g1.add_edge("a", "z")
        self.assertIn({"a", "z"}, self.g1.edge_collection)


if __name__ == "__main__":
    unittest.main()
