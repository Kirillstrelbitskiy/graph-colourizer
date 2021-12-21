"""
This module allows to colourize a graph in three colors (red, blue and green).
"""

from __future__ import unicode_literals
import doctest
import os
import argparse

# 2-sat find solution implementation


def dfs_type_1(graph):
    """
    First DFS used for typological sort.
    """

    order = []
    visited = set()

    for start in range(len(graph)):
        if start not in visited:
            stack = [(False, start)]
            visited.add(start)

            while stack:
                logical, vertex = stack.pop()
                if logical:
                    order.append(vertex)
                    continue

                stack.append((True, vertex))

                for child in graph[vertex]:
                    if child not in visited:
                        visited.add(child)
                        stack.append((False, child))

    return order


def dfs_type_2(start, color, components, graph):
    """
    Second DFS used for finding components in the graph.
    """

    stack = [start]
    components[start] = color

    while stack:
        vertex = stack.pop()

        for child in graph[vertex]:
            if components[child] == -1:
                components[child] = color
                stack.append(child)


def find_2_sat(graph):
    num_vertices = len(graph)
    components = [-1 for _ in range(num_vertices)]

    order = dfs_type_1(graph)

    color = 0
    for vertex in range(num_vertices):
        idx = order[num_vertices - vertex - 1]
        if components[idx] == -1:
            dfs_type_2(idx, color, components, graph)
            color += 1

    for vertex in range(0, num_vertices, 2):
        if components[vertex] == components[vertex + 1]:
            return None

    assigned_values = []
    for vertex in range(0, num_vertices, 2):
        assigned_values.append(components[vertex] > components[vertex + 1])

    return assigned_values


# Creating an graph of implications.

def vertex_idx(vertex, color, opp, num_colors):
    """
    Calculates a position of given vertex with specific color.

    >>> vertex_idx(1, 1, 1, 3)
    9
    """

    position = vertex * num_colors * 2
    position += color * 2 + opp

    return position


def build_implications_graph(initial_graph, initial_colors, num_colors):
    init_graph_sz = len(initial_colors)
    num_vertecies = init_graph_sz * num_colors * 2

    implications_graph = [[] for _ in range(num_vertecies)]

    # Type 1 clauses

    for edge in initial_graph:
        u_ver, v_ver = edge

        for color in range(num_colors):
            if color in (initial_colors[u_ver], initial_colors[v_ver]):
                continue

            implications_graph[vertex_idx(u_ver, color, 0, num_colors)].append(
                vertex_idx(v_ver, color, 1, num_colors))
            implications_graph[vertex_idx(v_ver, color, 0, num_colors)].append(
                vertex_idx(u_ver, color, 1, num_colors))

    # Type 2 & 3 clauses

    for vertex in range(init_graph_sz):
        for color1 in range(num_colors):
            for color2 in range(color1 + 1, num_colors):
                if initial_colors[vertex] in (color1, color2):
                    continue

                # Type 2 clauses

                implications_graph[vertex_idx(vertex, color1, 1, num_colors)].append(
                    vertex_idx(vertex, color2, 0, num_colors))
                implications_graph[vertex_idx(vertex, color2, 1, num_colors)].append(
                    vertex_idx(vertex, color1, 0, num_colors))

                # Type 3 clauses

                implications_graph[vertex_idx(vertex, color1, 0, num_colors)].append(
                    vertex_idx(vertex, color2, 1, num_colors))
                implications_graph[vertex_idx(vertex, color2, 0, num_colors)].append(
                    vertex_idx(vertex, color1, 1, num_colors))

    # Reversing implications graph because 2-SAT solver needs it

    reversed_graph = [[] for _ in range(num_vertecies)]
    for u_ver in range(num_vertecies):
        for v_ver in implications_graph[u_ver]:
            reversed_graph[v_ver].append(u_ver)

    return reversed_graph


# Finding solution

def read_data(file_path, colors_names):
    graph = []
    colors = {}

    num_verticies = 0

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            values = line.strip().split(',')

            u_ver, v_ver = int(values[0]) - 1, int(values[1]) - 1
            u_color, v_color = colors_names[values[2]], colors_names[values[3]]

            graph.append((u_ver, v_ver))

            colors[u_ver] = u_color
            colors[v_ver] = v_color

            num_verticies = max(num_verticies, max(u_ver, v_ver) + 1)

    final_colors = [-1 for _ in range(num_verticies)]
    for vertex in range(num_verticies):
        if vertex in colors:
            final_colors[vertex] = colors[vertex]

    return graph, final_colors


def find_colors(sat_solution, init_colors, num_colors, colors_names):
    num_vertices = len(init_colors)

    ans_colors = []
    for vertex in range(num_vertices):
        ver_color = -1

        for color in range(num_colors):
            idx = vertex * num_colors + color

            if sat_solution[idx] and color != init_colors[vertex]:
                ver_color = color

        if ver_color != -1:
            ans_colors.append((vertex + 1, colors_names[ver_color]))

    return ans_colors


def colourize_graph(initial_graph, initial_colors, colors_names):
    num_colors = 3

    implications_graph = build_implications_graph(
        initial_graph, initial_colors, num_colors)

    two_sat_solution = find_2_sat(implications_graph)

    if two_sat_solution == None:
        print("No solution")
        return

    ans_colors = find_colors(
        two_sat_solution, initial_colors, num_colors, colors_names)

    return ans_colors


def parse_file_path():
    parser = argparse.ArgumentParser(description='Graph Colourizer')
    parser.add_argument('-file', type=str, help='The path to a graph file')

    args = parser.parse_args()

    path_file = "graph.csv"
    if args.file:
        path_file = args.file

    if not os.path.isfile(path_file):
        print("A file with given path doesn't exist")
        exit()

    return path_file


def main():
    colors_names = {    
        'R': 0,
        'G': 1,
        'B': 2,
        0: 'R',
        1: 'G',
        2: 'B',
    }

    file_path = parse_file_path()

    initial_graph, initial_colors = read_data(file_path, colors_names)

    ans_colors = colourize_graph(initial_graph, initial_colors, colors_names)

    if ans_colors:
        print("Solution was found")
        print(ans_colors)


if __name__ == "__main__":
    main()

# doctest.testmod()
