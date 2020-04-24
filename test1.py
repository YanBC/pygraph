from graph import Graph

if __name__ == '__main__':
    graph_file = 'test1_graph.txt'

    g = Graph()
    g.initialize_from_file(graph_file)
    print(f'{g.to_dict()}\n')
    print(g)

    assert sorted(g.vertex_collection) == ['a', 'b', 'c', 'd', 'e', 'f']
    edges = g.edge_collection
    for e in [{'a', 'd'}, {'d', 'c'}, {'b', 'c'}, {'e', 'c'}]:
        assert e in edges

    assert sorted(g.get_adjacent_vertices('c')) == ['b', 'd', 'e']
    assert sorted(g.get_adjacent_vertices('x')) == [f'x not in graph']

    g.add_vertex('z')
    assert sorted(g.vertex_collection) == ['a', 'b', 'c', 'd', 'e', 'f', 'z'] 

    tmp_edge = {'a', 'z'}
    g.add_edge(tmp_edge)
    assert tmp_edge in g.edge_collection
