import os
import unittest

from graph import Graph

from .utils import current_dir

_test_graph2 = os.path.join(current_dir(__file__), "test2_graph.txt")


class TestGraphFind(unittest.TestCase):
    def setUp(self):
        self.g2 = Graph()
        self.g2.initialize_from_file(_test_graph2)

    def test_find_all_simple_paths_dfs_recursive(self):
        paths = self.g2.find_all_simple_paths_dfs_recursive("a", "b")
        for path in paths:
            self.assertIn(
                path,
                [["a", "d", "c", "b"], ["a", "f", "d", "c", "b"]],
            )

        paths = self.g2.find_all_simple_paths_dfs_recursive("a", "f")
        for path in paths:
            self.assertIn(
                path,
                [["a", "d", "f"], ["a", "f"]],
            )

        self.assertEqual(
            self.g2.find_all_simple_paths_dfs_recursive("c", "c"),
            [["c"]],
        )

    def test_find_cluster_dfs(self):
        self.assertEqual(
            self.g2.find_cluster_dfs("a"),
            ["a", "d", "c", "b", "e", "f"],
        )
        self.assertEqual(
            self.g2.find_cluster_dfs("b"),
            ["b", "c", "d", "a", "f", "e"],
        )
        self.assertEqual(
            self.g2.find_cluster_dfs("c"),
            ["c", "b", "d", "a", "f", "e"],
        )

    def test_find_simple_path_dfs(self):
        self.assertEqual(
            self.g2.find_simple_path_dfs("a", "b"),
            ["a", "d", "c", "b"],
        )

        paths = self.g2.find_all_simple_paths_dfs("a", "b")
        for path in paths:
            self.assertIn(
                path,
                [["a", "d", "c", "b"], ["a", "f", "d", "c", "b"]],
            )

        paths = self.g2.find_all_simple_paths_dfs("a", "f")
        for path in paths:
            self.assertIn(
                path,
                [["a", "d", "f"], ["a", "f"]],
            )

        self.assertEqual(
            self.g2.find_all_simple_paths_dfs("c", "c"),
            [["c"]],
        )

    def test_find_cluster(self):
        self.assertEqual(
            self.g2.find_cluster("a", "dfs"),
            ["a", "d", "c", "b", "e", "f"],
        )
        self.assertEqual(
            self.g2.find_cluster("b", "dfs"),
            ["b", "c", "d", "a", "f", "e"],
        )
        self.assertEqual(
            self.g2.find_cluster("c", "dfs"),
            ["c", "b", "d", "a", "f", "e"],
        )

        self.assertEqual(
            self.g2.find_cluster("a", "bfs"),
            ["a", "d", "f", "c", "b", "e"],
        )
        self.assertEqual(
            self.g2.find_cluster("b", "bfs"),
            ["b", "c", "d", "e", "a", "f"],
        )
        self.assertEqual(
            self.g2.find_cluster("c", "bfs"),
            ["c", "b", "d", "e", "a", "f"],
        )

    def test_find_simple_path(self):
        self.assertEqual(
            self.g2.find_simple_path("a", "b", "dfs"),
            ["a", "d", "c", "b"],
        )

        paths = self.g2.find_all_simple_paths("a", "b", "dfs")
        for path in paths:
            self.assertIn(
                path,
                [["a", "d", "c", "b"], ["a", "f", "d", "c", "b"]],
            )

        paths = self.g2.find_all_simple_paths("a", "f", "dfs")
        for path in paths:
            self.assertIn(
                path,
                [["a", "d", "f"], ["a", "f"]],
            )

        self.assertEqual(
            self.g2.find_all_simple_paths("c", "c", "dfs"),
            [["c"]],
        )

        self.assertEqual(
            self.g2.find_simple_path("a", "b", "bfs"),
            ["a", "d", "c", "b"],
        )

        paths = self.g2.find_all_simple_paths("a", "b", "bfs")
        for path in paths:
            self.assertIn(
                path,
                [["a", "d", "c", "b"], ["a", "f", "d", "c", "b"]],
            )

        paths = self.g2.find_all_simple_paths("a", "f", "bfs")
        for path in paths:
            self.assertIn(
                path,
                [["a", "d", "f"], ["a", "f"]],
            )

        self.assertEqual(
            self.g2.find_all_simple_paths("c", "c", "bfs"),
            [["c"]],
        )


if __name__ == "__main__":
    unittest.main()
