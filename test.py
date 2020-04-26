from graph import Graph

if __name__ == '__main__':
    ###########################
    # Test 1
    ###########################
    g1 = Graph()
    g1.initialize_from_file('test1_graph.txt')
    # print(f'{g1.to_dict()}\n')
    # print(g1)

    assert sorted(g1.vertex_collection) == ['a', 'b', 'c', 'd', 'e', 'f']
    edges = g1.edge_collection
    for e in [{'a', 'd'}, {'d', 'c'}, {'b', 'c'}, {'e', 'c'}]:
        assert e in edges

    assert sorted(g1.get_adjacent_vertices('c')) == ['b', 'd', 'e']
    assert sorted(g1.get_adjacent_vertices('x')) == [f'x not in graph']

    g1.add_vertex('z')
    assert sorted(g1.vertex_collection) == ['a', 'b', 'c', 'd', 'e', 'f', 'z'] 

    tmp_edge = {'a', 'z'}
    g1.add_edge(tmp_edge)
    assert tmp_edge in g1.edge_collection

    ###########################
    # Test 2
    ###########################
    g2 = Graph()
    g2.initialize_from_dict(g1.to_dict())

    assert g2.find_simple_path_dfs('a','b') == ['a', 'd', 'c', 'b']
    assert g2.find_all_simple_paths_dfs('a','b') == [['a', 'd', 'c', 'b']]
    assert g2.remove_vertex('c')

    g2.initialize_from_file('test2_graph.txt')
    # print(g2)

    paths = g2.find_all_simple_paths_dfs('a','b')
    for path in paths:
        assert path in [['a', 'd', 'c', 'b'], ['a', 'f', 'd', 'c', 'b']]

    paths = g2.find_all_simple_paths_dfs('a','f')
    for path in paths:
        assert path in [['a', 'd', 'f'], ['a', 'f']]

    assert g2.find_all_simple_paths_dfs('c','c') == [['c']]

    assert g2.find_cluster_dfs('a') == ['a', 'd', 'c', 'b', 'e', 'f']
    assert g2.find_cluster_dfs('b') == ['b', 'c', 'd', 'a', 'f', 'e']
    assert g2.find_cluster_dfs('c') == ['c', 'b', 'd', 'a', 'f', 'e']