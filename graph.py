from typing import Tuple, List, Set
from functools import lru_cache
from copy import deepcopy



'''
Abstract representation:
vertex:                         str
edge:                           Set[str]
path:                           List[str]

An undirected simple graph implementation
Graph._graph_dict:              Dict[Set[str]]

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
        ret_dict = deepcopy(self._graph_dict)
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
                self._remove_edge({node_a, node_b})

            self._graph_dict.pop(vertex_tobe_remove)
            return True
        else:
            return False


    def add_edge(self, vertex_a:str, vertex_b:str) -> bool:
        return self._add_edge({vertex_a, vertex_b})


    def remove_edge(self, vertex_a:str, vertex_b:str) -> bool:
        return self._remove_edge({vertex_a, vertex_b})


    def _add_edge(self, new_edge:Set[str]) -> bool:
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


    def _remove_edge(self, edge_tobe_removed:Set[str]) -> bool:
        node_a, node_b = edge_tobe_removed
        if node_a in self._graph_dict[node_b] and node_b in self._graph_dict[node_a]:
            self._graph_dict[node_a].remove(node_b)
            self._graph_dict[node_b].remove(node_a)
            return True
        else:
            return False


    def initialize_from_dict(self, d:dict) -> bool:
        self._graph_dict = deepcopy(d)
        return True


    def initialize_from_file(self, filePath:str, delimiter:str=' ') -> bool:
        try:
            f = open(filePath)
        except FileNotFoundError:
            print(f'File not exits: {filePath}')
            return False

        self._graph_dict = dict()
        edge_strs = f.readlines()
        for edge_str in edge_strs:
            v_list = edge_str.strip().split(delimiter)
            if len(v_list) == 1:
                self.add_vertex(v_list[0])
            elif len(v_list) == 2:
                self._add_edge({v_list[0], v_list[1]})
            else:
                pass
        return True


    def get_adjacent_vertices(self, vertex:str) -> List[str]:
        if vertex in self.vertex_collection:
            return list(self._graph_dict[vertex])
        else:
            return [f'{vertex} not in graph']


    # This function can potentially run faster if introduced a 
    # visted list which keeps track of all visited nodes
    def find_simple_path_dfs_recursive(self, start_vertex:str, end_vertex:str, track:List[str]=None) -> List[str]:
        if track is None:
            all_vertices = self.vertex_collection
            if (start_vertex not in all_vertices) or (end_vertex not in all_vertices):
                return None
            track = [start_vertex]

        if start_vertex == end_vertex:
            return track

        for vertex in self._graph_dict[start_vertex]:
            if not (vertex in track):
                tmp_track = track + [vertex]
                path = self.find_simple_path_dfs_recursive(vertex, end_vertex, tmp_track)
                if path is not None:
                    return path
        return None


    def find_all_simple_paths_dfs_recursive(self, start_vertex:str, end_vertex:str, track:List[str]=None) -> List[List[str]]:
        if track is None:
            all_vertices = self.vertex_collection
            if (start_vertex not in all_vertices) or (end_vertex not in all_vertices):
                return None
            track = [start_vertex]

        if start_vertex == end_vertex:
            return [track]

        all_paths = []
        for vertex in self._graph_dict[start_vertex]:
            if vertex not in track:
                tmp_track = track + [vertex]
                all_paths += self.find_all_simple_paths_dfs_recursive(vertex, end_vertex, tmp_track)
        return all_paths


    def find_cluster_dfs(self, vertex:str) -> List[str]:
        if not vertex in self.vertex_collection:
            return []

        vertices = []
        stack = [vertex]
        visited = [vertex]

        while stack:
            node = stack.pop()
            vertices.append(node)

            for adjacent in sorted(list(self._graph_dict[node]), reverse=True):
                if adjacent not in visited:
                    visited.append(adjacent)
                    stack.append(adjacent)

        return vertices


    def find_all_clusters_dfs(self) -> List[Set[str]]:
        clusters = []
        for v in self.vertex_collection:
            c = set(self.find_cluster_dfs(v))
            if c not in clusters:
                clusters.append(c)
        return clusters


    def find_simple_path_dfs(self, start_vertex:str, end_vertex:str) -> List[str]:
        all_vertices = self.vertex_collection
        if (start_vertex not in all_vertices) or (end_vertex not in all_vertices):
            return []

        stack = [[start_vertex]]
        visited = [start_vertex]
        
        while stack:
            path = stack.pop()
            node = path[-1]
            if node == end_vertex:
                return path

            for adjacent in sorted(list(self._graph_dict[node]), reverse=True):
                if adjacent not in visited:
                    visited.append(adjacent)
                    stack.append(path + [adjacent])
        
        return []

 
    def find_all_simple_paths_dfs(self, start_vertex:str, end_vertex:str) -> List[List[str]]:
        all_vertices = self.vertex_collection
        if (start_vertex not in all_vertices) or (end_vertex not in all_vertices):
            return []

        stack = [[start_vertex]]
        all_paths = []

        while stack:
            path = stack.pop()
            node = path[-1]
            if node == end_vertex:
                all_paths.append(path)
                continue

            for adjacent in sorted(list(self._graph_dict[node]), reverse=True):
                if adjacent not in path:
                    stack.append(path + [adjacent])

        return all_paths


    def is_connected_with_dfs(self, vertex_a:str, vertex_b:str) -> bool:
        all_vertices = self.vertex_collection
        if (vertex_a not in all_vertices) or (vertex_b not in all_vertices):
            return False

        stack = [vertex_a]
        visited = [vertex_a]

        while stack:
            node = stack.pop()
            if node == vertex_b:
                return True

            for adjacent in sorted(list(self._graph_dict[node]), reverse=True):
                if adjacent not in visited:
                    visited.append(adjacent)
                    stack.append(adjacent)

        return False


    def find_cluster_bfs(self, vertex:str) -> List[str]:
        if not vertex in self.vertex_collection:
            return []

        vertices = []
        stack = [vertex]
        visited = [vertex]

        while stack:
            node = stack.pop(0)
            vertices.append(node)

            for adjacent in sorted(list(self._graph_dict[node]), reverse=False):
                if adjacent not in visited:
                    visited.append(adjacent)
                    stack.append(adjacent)

        return vertices


    # new universal search methods
    def _func_search_check_input(self, mode:str, *args) -> bool:
        if mode not in ['dfs', 'bfs']:
            return False
        for vertex in args:
            if vertex not in self.vertex_collection:
                return False
        return True


    def _func_search_parse_mode(self, mode:str) -> Tuple:
        if mode == 'dfs':
            stack_pop_index = -1
            sort_order_reverse = True
        elif mode == 'bfs':
            stack_pop_index = 0
            sort_order_reverse = False
        return stack_pop_index, sort_order_reverse
        

    def find_cluster(self, vertex:str, mode:str='dfs') -> List[str]:
        if not self._func_search_check_input(mode, vertex):
            raise ValueError('please check your input arguments')
        pop_index, order_reverse = self._func_search_parse_mode(mode)

        vertices = []
        stack = [vertex]
        visited = [vertex]

        while stack:
            node = stack.pop(pop_index)
            vertices.append(node)

            for adjacent in sorted(list(self._graph_dict[node]), reverse=order_reverse):
                if adjacent not in visited:
                    visited.append(adjacent)
                    stack.append(adjacent)

        return vertices


    def find_all_clusters(self, mode:str='dfs') -> List[Set[str]]:
        if not self._func_search_check_input(mode):
            raise ValueError('please check your input arguments')

        clusters = []
        for v in self.vertex_collection:
            c = set(self.find_cluster(v, mode))
            if c not in clusters:
                clusters.append(c)
        return clusters


    def find_simple_path(self, start_vertex:str, end_vertex:str, mode:str='dfs') -> List[str]:
        if not self._func_search_check_input(mode, start_vertex, end_vertex):
            raise ValueError('please check your input arguments')
        pop_index, order_reverse = self._func_search_parse_mode(mode)

        stack = [[start_vertex]]
        visited = [start_vertex]
        
        while stack:
            path = stack.pop(pop_index)
            node = path[-1]
            if node == end_vertex:
                return path

            for adjacent in sorted(list(self._graph_dict[node]), reverse=order_reverse):
                if adjacent not in visited:
                    visited.append(adjacent)
                    stack.append(path + [adjacent])
        
        return []

 
    def find_all_simple_paths(self, start_vertex:str, end_vertex:str, mode:str='dfs') -> List[List[str]]:
        if not self._func_search_check_input(mode, start_vertex, end_vertex):
            raise ValueError('please check your input arguments')
        pop_index, order_reverse = self._func_search_parse_mode(mode)

        stack = [[start_vertex]]
        all_paths = []

        while stack:
            path = stack.pop(pop_index)
            node = path[-1]
            if node == end_vertex:
                all_paths.append(path)
                continue

            for adjacent in sorted(list(self._graph_dict[node]), reverse=order_reverse):
                if adjacent not in path:
                    stack.append(path + [adjacent])

        return all_paths


    def is_connected_with(self, vertex_a:str, vertex_b:str, mode:str='dfs') -> bool:
        if not self._func_search_check_input(mode, vertex_a, vertex_b):
            raise ValueError('please check your input arguments')
        pop_index, order_reverse = self._func_search_parse_mode(mode)

        stack = [vertex_a]
        visited = [vertex_a]

        while stack:
            node = stack.pop(pop_index)
            if node == vertex_b:
                return True

            for adjacent in sorted(list(self._graph_dict[node]), reverse=order_reverse):
                if adjacent not in visited:
                    visited.append(adjacent)
                    stack.append(adjacent)

        return False





