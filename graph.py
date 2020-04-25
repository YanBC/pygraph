from typing import Tuple, List, Set
from functools import lru_cache




'''
Abstract representation:
vertex:     str
edge:        Set[str]
path:        List[str]

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

    def add_vertex(self, new_vertex:str) -> bool:
        if new_vertex not in self.vertex_collection:
            self._graph_dict[new_vertex] = set()
            return True
        else:
            return False

    def remove_vertex(self, vertex_tobe_remove:str) -> bool:
        if vertex_tobe_remove in self.vertex_collection:
            adjacent_vertices = list(self._graph_dict[vertex_tobe_remove])

            node_a = vertex_tobe_remove
            for node_b in adjacent_vertices:
                self.remove_edge({node_a, node_b})

            self._graph_dict.pop(vertex_tobe_remove)
            return True
        else:
            return False

    def add_edge(self, new_edge:Set[str]) -> bool:
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

    def remove_edge(self, edge_tobe_removed:Set[str]) -> bool:
        node_a, node_b = edge_tobe_removed
        if node_a in self._graph_dict[node_b] and node_b in self._graph_dict[node_a]:
            self._graph_dict[node_a].remove(node_b)
            self._graph_dict[node_b].remove(node_a)
            return True
        else:
            return False

    def initialize_from_dict(self, d:dict) -> bool:
        self._graph_dict = d
        return True

    def initialize_from_file(self, filePath:str, delimiter:str=' ') -> bool:
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

    def get_adjacent_vertices(self, vertex:str) -> List[str]:
        if vertex in self.vertex_collection:
            return list(self._graph_dict[vertex])
        else:
            return [f'{vertex} not in graph']

    def find_simple_path_dfs(self, start_vertex:str, end_vertex:str, track:List[str]=None) -> List[str]:
        if track is None:
            track = [start_vertex]

        if start_vertex == end_vertex:
            return track

        for vertex in self._graph_dict[start_vertex]:
            if not (vertex in track):
                tmp_track = track + [vertex]
                path = self.find_simple_path_dfs(vertex, end_vertex, tmp_track)
                if path is not None:
                    return path
        return None

    def find_all_simple_paths_dfs(self, start_vertex:str, end_vertex:str, track:List[str]=None) -> List[List[str]]:
        if track is None:
            track = [start_vertex]

        if start_vertex == end_vertex:
            return [track]

        all_paths = []
        for vertex in self._graph_dict[start_vertex]:
            if vertex not in track:
                tmp_track = track + [vertex]
                all_paths += self.find_all_simple_paths_dfs(vertex, end_vertex, tmp_track)
        return all_paths

