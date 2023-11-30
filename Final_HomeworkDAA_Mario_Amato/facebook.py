from utility import *
from graph import *


def facebook_enmy(V, E):
    max = 0
    reference = None
    for edge in E:
        if E[edge] > max:
            max = E[edge]
            reference = edge

    D = set()
    R = set()
    V.remove(reference[0])
    V.remove(reference[1])
    D.add(reference[0])
    R.add(reference[1])

    for i in V:
        w_F = 0
        w_S = 0
        for j in D:
            if (i, j) in E.keys() and j != i:
                w_F += E[(i, j)]
            elif (j, i) in E.keys() and j != i:
                w_F += E[(j, i)]
        for j in R:
            if (i, j) in E.keys() and j != i:
                w_S += E[(i, j)]
            elif (j, i) in E.keys() and j != i:
                w_S += E[(j, i)]

        if w_F >= w_S:
            R.add(i)
        else:
            D.add(i)

    return D, R


def facebook_friend(V, E):
    G = create_graph(V, E)
    D = set()
    R = set()

    super_source = G.insert_vertex("source")
    super_sink = G.insert_vertex("sink")

    # Link super source and super sink to all the nodes and create a first residual graph
    first_compute(G, V, super_source, super_sink)

    # Create the entire residual graph
    nodes = []
    incident_edge = G.incident_edges(super_source)
    for edge in incident_edge:
        nodes.append(edge.get_destination())

    for vertex in nodes:
        friendship = G.get_edge(super_source, vertex).element()
        found_flow = 0

        while found_flow < friendship:
            incremental_path, add_flow = augment(G, vertex, super_sink, friendship - found_flow)
            if not incremental_path:
                break
            found_flow += add_flow
        if found_flow == friendship:
            G.remove_edge(super_source, vertex)

    discovered = {}
    # start the bfs from the source so I can figure out which voter is part of the Democrats
    BFS(G, super_source, discovered)
    if super_source in discovered:
        del discovered[super_source]

    for v in discovered:
        D.add(v.element())
    R = (V.keys() - D)

    return D, R


def first_compute(G, V, source, sink):
    for vertex in G.vertices():
        if vertex is not source and vertex is not sink:
            ValD = V[vertex.element()][0]
            ValR = V[vertex.element()][1]
            bottleneck = min(ValD, ValR)
            D_sub = ValD - bottleneck
            R_sub = ValR - bottleneck
            if D_sub > 0:
                G.insert_edge(source, vertex, D_sub)
            elif R_sub > 0:
                G.insert_edge(vertex, sink, R_sub)
            else:
                pass


def create_graph(V, E):
    G = Graph(True)
    S = {}
    for voter in V.keys():
        S[voter] = G.insert_vertex(voter)
    for friendship in E:
        if E.get(friendship) == 0:
            continue
        G.insert_edge(S.__getitem__(friendship[0]), S.__getitem__(friendship[1]), E.get(friendship))
        G.insert_edge(S.__getitem__(friendship[1]), S.__getitem__(friendship[0]), E.get(friendship))
    return G
