from graph import Graph

if __name__ == '__main__':
    ###########################
    # Test 1
    ###########################
    graph_file1 = 'test1_graph.txt'

    g1 = Graph()
    g1.initialize_from_file(graph_file)
    print(f'{g1.to_dict()}\n')
    print(g1)

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
    assert g1.find_simple_path_dfs('a','b') == ['a', 'd', 'c', 'b']
    assert g1.find_all_simple_paths_dfs('a','b') == [['a', 'd', 'c', 'b']]
    assert g1.remove_vertex('c')



