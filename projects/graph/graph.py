debug = False

"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def __str__(self):
        return str(self.vertices)

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        if vertex_id not in self.vertices:
            self.vertices[vertex_id] = set()
        else:
            if debug: print(f"Vertex {vertex_id} is already in the Graph")

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if (v1 or v2) not in self.vertices:
            target = None
            if v1 not in self.vertices:
                target = v1
            elif v2 not in self.vertices:
                target = v2
            raise Exception(f"Vertex {target} does not exist in the Graph")
        else:
            self.vertices[v1].add(v2)

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        n = self.vertices[vertex_id]
        if debug: print(f"Neighbors:\t{n}")
        return n

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        # queue / dequeue

        ## make a queue of vertices to visit
        q = Queue()

        ## make a set to track visited separately
        visited = set()

        ## enqueue entrypoint vertex onto queue
        q.enqueue(starting_vertex)

        sz = q.size()
        ## while queue isn't empty
        while sz > 0:
            if debug: print(f"Queue: size={sz}\t{q}")

            ### dequeue first vertex as current
            current_node = q.dequeue()

            ### if not visited
            if current_node not in visited:
                if debug:
                    print(f"Current:\t{current_node}")
                else:
                    print(current_node)

                #### add to visited set
                if debug: print(f"Visited:\t{visited}")
                visited.add(current_node)
                if debug: print(f"Visited:  + {current_node}\t{visited}")

                #### get neighbors
                neighbors = self.get_neighbors(current_node)

                #### enqueue neighbors
                if debug: print(f"Queue before:\t{q}")
                for neighbor in neighbors:
                    q.enqueue(neighbor)
                if debug: print(f"Queue after:\t{q}")

            sz = q.size()

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        # stack / pop

        ## make stack of vertices to visit
        s = Stack()

        ## make set to track visited separately
        visited = set()

        ## push entrypoint vertex onto stack
        s.push(starting_vertex)

        sz = s.size()
        ## while stack isn't empty
        while sz > 0:
            if debug: print(f"Stack: size={sz}\t{s}")

            ### pop off top stack entry as current
            current_node = s.pop()

            ### if not visited
            if current_node not in visited:
                if debug:
                    print(f"Current:\t{current_node}")
                else:
                    print(current_node)

                #### add to visited set
                if debug: print(f"Visited:\t{visited}")
                visited.add(current_node)
                if debug: print(f"Visited:  + {current_node}\t{visited}")

                #### get neighbors
                neighbors = self.get_neighbors(current_node)

                #### put neighbors on stack
                if debug: print(f"Stack before:\t{s}")
                for neighbor in neighbors:
                    s.push(neighbor)
                if debug: print(f"Stack after:\t{s}")

            sz = s.size()

    def dft_recursive(self, starting_vertex, visited=set()):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        if starting_vertex in visited:
            return
        else:
            visited.add(starting_vertex)
            if debug:
                print(f"vertex:\t\t{starting_vertex}")
            else:
                print(starting_vertex)

            neighbors = self.get_neighbors(starting_vertex)

            for neighbor in neighbors:
                self.dft_recursive(neighbor, visited)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        q = Queue()
        visited = set()

        q.enqueue(starting_vertex)

        while q.size() > 0:
            if debug: print(f"Queue:\t\t{q}")
            current_path = q.dequeue()
            if debug: print(f"current_path\t{current_path}")
            if isinstance(current_path, list):
                current_vertex = current_path[-1]
            elif isinstance(current_path, int):
                current_vertex = current_path

            if debug: print(f"current_vertex\t{current_vertex}\tdestination_vertex\t{destination_vertex}")
            if current_vertex == destination_vertex:
                return current_path

            if current_vertex not in visited:
                visited.add(current_vertex)

                neighbors = self.get_neighbors(current_vertex)
                if debug: print(f"neighbors\t{neighbors}")

                for neighbor in neighbors:
                    if isinstance(current_path, list):
                        path_copy = current_path + [neighbor]
                    elif isinstance(current_path, int):
                        path_copy = []
                        path_copy.append(current_path)
                        path_copy.append(neighbor)
                    if debug: print(f"path_copy\t{path_copy}")
                    q.enqueue(path_copy)

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        s = Stack()
        visited = set()

        s.push(starting_vertex)

        while s.size() > 0:
            if debug: print(f"Stack:\t\t{s}")
            current_path = s.pop()
            if debug: print(f"current_path\t{current_path}")
            if isinstance(current_path, list):
                current_vertex = current_path[-1]
            elif isinstance(current_path, int):
                current_vertex = current_path

            if debug: print(f"current_vertex\t{current_vertex}\tdestination_vertex\t{destination_vertex}")
            if current_vertex == destination_vertex:
                return current_path

            if current_vertex not in visited:
                visited.add(current_vertex)

                neighbors = self.get_neighbors(current_vertex)
                if debug: print(f"neighbors\t{neighbors}")

                for neighbor in neighbors:
                    if isinstance(current_path, list):
                        path_copy = current_path + [neighbor]
                    elif isinstance(current_path, int):
                        path_copy = []
                        path_copy.append(current_path)
                        path_copy.append(neighbor)
                    if debug: print(f"path_copy\t{path_copy}")
                    s.push(path_copy)

    def dfs_recursive(self, starting_vertex, destination_vertex, visited=set(), path=[]):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """

        path = path + [starting_vertex]
        if debug: print(f"path\t\t{path}")

        # Base case
        if starting_vertex == destination_vertex:
            if debug: print("found match!")
            return path

        # Recursive case
        if starting_vertex not in visited:
            visited.add(starting_vertex)
            if debug: print(f"visited\t\t{visited}")
            for vertex in self.get_neighbors(starting_vertex):
                if debug: print(f"vertex\t\t{vertex}")
                next_path = self.dfs_recursive(vertex, destination_vertex, visited, path)
                if debug: print(f"next_path\t{next_path}")
                if next_path:
                    return next_path

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(f"Vertices:\t{graph.vertices}")

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    print("bft")
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    print("dft")
    graph.dft(1)
    print("dft_recursive")
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print("bfs")
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print("dfs")
    print(graph.dfs(1, 6))
    print("dfs_recursive")
    print(graph.dfs_recursive(1, 6))
