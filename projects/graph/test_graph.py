debug = False

import unittest
import sys
import io
from graph import Graph

class Test(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()

        self.graph.add_vertex(1)
        self.graph.add_vertex(2)
        self.graph.add_vertex(3)
        self.graph.add_vertex(4)
        self.graph.add_vertex(5)
        self.graph.add_vertex(6)
        self.graph.add_vertex(7)
        
        self.graph.add_edge(5, 3)
        self.graph.add_edge(6, 3)
        self.graph.add_edge(7, 1)
        self.graph.add_edge(4, 7)
        self.graph.add_edge(1, 2)
        self.graph.add_edge(7, 6)
        self.graph.add_edge(2, 4)
        self.graph.add_edge(3, 5)
        self.graph.add_edge(2, 3)
        self.graph.add_edge(4, 6)

    def test_vertices(self):
        print("\ntest_vertices")
        vertices = {
            1: {2},
            2: {3, 4},
            3: {5},
            4: {6, 7},
            5: {3},
            6: {3},
            7: {1, 6}
        }
        if debug: print(f"vertices:\n{vertices}")
        output = self.graph.vertices
        if debug: print(f"output:\n{output}")
        self.assertDictEqual(output, vertices)

    def test_bft(self):
        print("\ntest_bft")
        bft = [
            "1\n2\n3\n4\n5\n6\n7\n",
            "1\n2\n3\n4\n5\n7\n6\n",
            "1\n2\n3\n4\n6\n7\n5\n",
            "1\n2\n3\n4\n6\n5\n7\n",
            "1\n2\n3\n4\n7\n6\n5\n",
            "1\n2\n3\n4\n7\n5\n6\n",
            "1\n2\n4\n3\n5\n6\n7\n",
            "1\n2\n4\n3\n5\n7\n6\n",
            "1\n2\n4\n3\n6\n7\n5\n",
            "1\n2\n4\n3\n6\n5\n7\n",
            "1\n2\n4\n3\n7\n6\n5\n",
            "1\n2\n4\n3\n7\n5\n6\n"
        ]

        stdout_ = sys.stdout
        sys.stdout = io.StringIO()
        self.graph.bft(1)
        output = sys.stdout.getvalue()

        if debug: print(f"output:\n{output}")
        self.assertIn(output, bft)

        sys.stdout = stdout_  # Restore stdout

    def test_dft(self):
        print("\ntest_dft")
        dft = [
            "1\n2\n3\n5\n4\n6\n7\n",
            "1\n2\n3\n5\n4\n7\n6\n",
            "1\n2\n4\n7\n6\n3\n5\n",
            "1\n2\n4\n6\n3\n5\n7\n"
        ]

        stdout_ = sys.stdout
        sys.stdout = io.StringIO()
        self.graph.dft(1)
        output = sys.stdout.getvalue()

        if debug: print(f"output:\n{output}")
        self.assertIn(output, dft)

        sys.stdout = stdout_  # Restore stdout

    def test_dft_recursive(self):
        print("\ntest_dft_recursive")
        dft = [
            "1\n2\n3\n5\n4\n6\n7\n",
            "1\n2\n3\n5\n4\n7\n6\n",
            "1\n2\n4\n7\n6\n3\n5\n",
            "1\n2\n4\n6\n3\n5\n7\n"
        ]

        stdout_ = sys.stdout
        sys.stdout = io.StringIO()
        self.graph.dft_recursive(1)
        output = sys.stdout.getvalue()

        if debug: print(f"output:\n{output}")
        self.assertIn(output, dft)

        sys.stdout = stdout_  # Restore stdout

    def test_bfs(self):
        print("\ntest_bfs")
        bfs = [1, 2, 4, 6]
        output = self.graph.bfs(1, 6)
        if debug: print(f"output:\n{output}")
        self.assertListEqual(output, bfs)

    def test_dfs(self):
        print("\ntest_dfs")
        dfs = [
            [1, 2, 4, 6],
            [1, 2, 4, 7, 6]
        ]
        output = self.graph.dfs(1, 6)
        if debug: print(f"output:\n{output}")
        self.assertIn(output, dfs)

    def test_dfs_recursive(self):
        print("\ntest_dfs_recursive")
        dfs = [
            [1, 2, 4, 6],
            [1, 2, 4, 7, 6]
        ]
        output = self.graph.dfs_recursive(1, 6)
        if debug: print(f"output:\n{output}")
        self.assertIn(output, dfs)

if __name__ == '__main__':
    unittest.main()
