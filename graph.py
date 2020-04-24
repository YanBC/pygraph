from typing import Tuple, List, Set
from functools import lru_cache




'''
vertext is represented by a str
edge is represented by a Set[str]

A undirected simple graph implementation

'''
class Graph(object):
    def __init__(self):
        self._graph_dict = dict()

    def __repr__(self):
        edge_list = [list(edge) for edge in self.edge_collection]
        edge_list = sorted(edge_list)

        graph_str = f'Vertices: {sorted(self.vertex_collection)}\n'
        graph_str += 'Edges:\n'
        for edge in edge_list:
            graph_str += f'    {edge[0]} -- {edge[1]}\n'

        return graph_str

    #################
    # properties
    #################
    @property
    def vertex_collection(self) -> list:
        return list(self._graph_dict.keys())

    @property
    def edge_collection(self) -> list:
        all_edges = []
        for vertex_a in self.vertex_collection:
            for vertex_b in self._graph_dict[vertex_a]:
                tmp_edge = {vertex_a, vertex_b}
                if tmp_edge not in all_edges:
                    all_edges.append(tmp_edge)
        return all_edges

    #################
    # methods
    #################
    def to_dict(self) -> dict:
        ret_dict = self._graph_dict.copy()
        return ret_dict

    def add_vertex(self, new_vertex: str) -> bool:
        if new_vertex not in self.vertex_collection:
            self._graph_dict[new_vertex] = set()
            return True
        else:
            return False

    def add_edge(self, new_edge: Set[str]) -> bool:
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
            if not (new_edge in self.edge_collection):
                self._graph_dict[node_a].add(node_b)
                self._graph_dict[node_b].add(node_a)
                return True
        return False

    def initialize_from_dict(self, d: dict) -> bool:
        self._graph_dict = d
        return True

    def initialize_from_file(self, filePath: str, delimiter: str = ' ') -> bool:
        try:
            f = open(filePath)
        except FileNotFoundError:
            print(f'File not exits: {filePath}')
            return False

        edge_strs = f.readlines()
        for edge_str in edge_strs:
            v_list = edge_str.strip().split(delimiter)
            if len(v_list) == 1:
                self.add_vertex(v_list[0])
            elif len(v_list) == 2:
                self.add_edge({v_list[0], v_list[1]})
            else:
                pass
        return True



