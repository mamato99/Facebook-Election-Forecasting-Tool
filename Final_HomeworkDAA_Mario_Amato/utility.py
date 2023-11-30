# Copyright 2013, Michael H. Goldwasser
#
# Developed for use with the book:
#
#    Data Structures and Algorithms in Python
#    Michael T. Goodrich, Roberto Tamassia, and Michael H. Goldwasser
#    John Wiley & Sons, 2013
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from math import inf


def BFS(g, s, discovered):
    """Perform BFS of the undiscovered portion of Graph g starting at Vertex s.

    discovered is a dictionary mapping each vertex to the edge that was used to
    discover it during the BFS (s should be mapped to None prior to the call).
    Newly discovered vertices will be added to the dictionary as a result.
    """
    level = [s]  # first level includes only s
    while len(level) > 0:
        next_level = []  # prepare to gather newly found vertices
        for u in level:
            for e in g.incident_edges(u):  # for every outgoing edge from u
                v = e.opposite(u)
                if v not in discovered:  # v is an unvisited vertex
                    discovered[v] = e  # e is the tree edge that discovered v
                    next_level.append(v)  # v will be further considered in next pass
        level = next_level  # relabel 'next' level to become current


def modified_BFS(g, s, stop, discovered):
    """Perform BFS of the undiscovered portion of Graph g starting at Vertex s
    and stopping when the Vertex stop is found.

    discovered is a dictionary mapping each vertex to the edge that was used to
    discover it during the BFS (s should be mapped to None prior to the call).
    Newly discovered vertices will be added to the dictionary as a result.
    """
    level = [s]  # first level includes only s
    while len(level) > 0:
        next_level = []  # prepare to gather newly found vertices
        for u in level:
            for e in g.incident_edges(u):  # for every outgoing edge from u
                v = e.opposite(u)
                if v not in discovered:  # v is an unvisited vertex
                    if v is stop:
                        discovered[v] = e
                        return
                    discovered[v] = e  # e is the tree edge that discovered v
                    next_level.append(v)  # v will be further considered in next pass
        level = next_level  # relabel 'next' level to become current


def construct_path(u, v, discovered):
    route = []  # empty path by default
    bottleneck = +inf

    if v in discovered:  # we build list from v to u and then reverse it at the end
        route.append(v)
        walk = v
        while walk is not u:
            e = discovered[walk]  # find edge leading to walk
            if e.element() < bottleneck:
                bottleneck = e.element()
            parent = e.opposite(walk)
            route.append(parent)
            walk = parent
        route.reverse()  # reorient path from u to v
    return route, bottleneck


def augment(G, source, sink, remaining):
    route, bott = bottleneck_calculation(G, source, sink)

    bottleneck = min(remaining, bott)

    if len(route) == 0 or route[-1] is not sink:
        return False, 0

    for i in range(len(route) - 1):
        u = route[i]
        v = route[i + 1]

        forward = G.get_edge(u, v)
        decrement = forward.element() - bottleneck
        if decrement == 0:
            G.remove_edge(u, v)
        else:
            forward.set_element(decrement)
        #if the arc is connected either to the source or to the sink the backward edge is not inserted
        if v.element() == 'source' or v.element() == 'sink' or u.element() == 'source' or u.element() == 'sink':
            pass
        else:
            backward = G.get_edge(v, u)
            if backward is None:
                G.insert_edge(v, u, bottleneck)
            else:
                increment = backward.element() + bottleneck
                backward.set_element(increment)

    return True, bottleneck


def bottleneck_calculation(g, start, stop):
    connected = {}
    modified_BFS(g, start, stop, connected)
    path, bott = construct_path(start, stop, connected)
    return path, bott
