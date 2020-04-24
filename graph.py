from typing import Tuple, List

# A undirected simple graph implementation
class Graph(object):
    def __init__(self):
        self._graph_dict = dict()

    @property
    def vertex_collection(self):
        return list(self._graph_dict.keys())

    def add_vertex(self, new_vertex: str):
        if new_vertex not in self.vertex_collection:
            self._graph_dict[new_vertex] = set()
            return True
        else:
            return False

    def _are_the_same_edges(self, edge_a: Tuple[str], edge_b: Tuple[str]):
        tmp_a = set(edge_a)
        tmp_b = set(edge_b)
        if tmp_a == tmp_b:
            return True
        else:
            return False

    def _edge_is_in(self, edge: Tuple[str], edge_list: List[Tuple[str]]):
        for existing_edge in edge_list:
            if self._are_the_same_edges(existing_edge, edge):
                return True
        return False

    @property
    def edge_collection(self):
        all_edges = []
        for vertex_a in self.vertex_collection:
            for vertex_b in self._graph_dict[vertex_a]:
                all_edges.append((vertex_a, vertex_b))

        ret_edges = []
        for edge in all_edges:
            if not self._edge_is_in(edge, ret_edges):
                ret_edges.append(edge)

        return ret_edges
        
    def add_edge(self, new_edge: Tuplep[str]):
        node_a, node_b = new_edge
        vertices = self.vertex_collection
        a_is_new = node_a not in vertices
        b_is_new = node_b not in vertices

        if a_is_new or b_is_new:
            if a_is_new:
                self.add_vertex(node_a)
            if b_is_new:
                self.add_vertex(node_b)
            self._graph_dict[node_a].add(node_b)
            self._graph_dict[node_b].add(node_a)
            return True
        else:
            if self._edge_is_in(new_edge, self.edge_collection):
                return False
            else:
                self._graph_dict[node_a].add(node_b)
                self._graph_dict[node_b].add(node_a)
                return True

    def __repr__(self):
        edge_list = self.edge_collection

        graph_str = f'Vertices: {self.vertex_collection}\n'
        graph_str += 'Edges:\n'
        for edge in edge_list:
            graph_str += f'{edge[0]} -- {edge[1]}\n'

        return graph_str

    @property
    def graph_as_dict(self):
        ret_dict = self._graph_dict.copy()
        return ret_dict

    def initialize_from_dict(self, d: dict):
        self._graph_dict = d
        return True

    def initialize_from_file(self, filePath: str, delimiter: str = ' '):
        try:
            f = open(filePath)
        except FileNotFoundError:
            print(f'File not exits: {filePath}')
            return False

        edge_strs = f.readlines()
        for edge_str in edge_strs:
            vertex_list = edge_str.split(delimiter)
            if len(vertex_list) == 1:
                self.add_vertex(vertex_list[0])
            elif len(vertex_list) == 2:
                self.add_edge((vertex_list[0], vertex_list[1]))
            else:
                pass
        return True