import math
import itertools

# Adjacency matrix.
graph = [
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, -10, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 10, 1, 1, 1, 1],
    [1, 1, 1, 1, 10, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 0]]

# Number of nodes in the graph.
n = len(graph)
# Number of nodes that are optional in our black box (S collection).
l = n - 1

def find_nodes_in_b_box(bin_num):
    # Convert binary num to array.
    nodes_model = [str(x) for x in str(bin_num)]
    b_box_nodes = []
    # Save indexes of nodes that are represent by "1" in black box.
    for i in range(len(nodes_model)):
        if nodes_model[i] == "1":
            b_box_nodes.append(i+2)
    return b_box_nodes

def count_distance_cost(v1, v2, graph):
    # Return cost of given edge in given graph.
    return graph[v1][v2]

def count_complex_distance_cost(start, b_b_nodes, k, graph):
    smallest_cost = math.inf
    beg = start
    best_fit = None
    permutation_nodes = list(itertools.permutations(b_b_nodes))
    # Iterate through permutations.
    for per in range(len(permutation_nodes)):
        # Set initial values in each permutation.
        distance = 0
        start = beg
        for node in range(len(permutation_nodes[per])):
            distance += count_distance_cost(start, permutation_nodes[per][node]-1, graph)
            start = permutation_nodes[per][node]-1
        distance += count_distance_cost(start, k, graph)
        if distance < smallest_cost:
            smallest_cost = distance
            best_fit = permutation_nodes[per]
    return smallest_cost, best_fit

if __name__ == "__main__":

    # Initialize number to binary conversion (black box representation).
    num = 0
    # Initialize shortest_path that we are looking for.
    shortest_path =	{"nodes": [], "path_cost": math.inf}
    # Initialize current distance variable.
    distance = 0
    # Maximal num that we can write to 2**l bits (decimal).
    max_num = 2 ** l
    # Omit situation when all bits are set to 1, because every node is visited exactly once.
    for i in range(max_num):
        # Convert decimal representation of number to binary.
        bin_num_rep = bin(num)[2:].zfill(l)
        # Increase num to binary conversion representing black box.
        num += 1
        # Iterate through nodes, except 1st one.
        for k in range(2, n+1):
            # Represent nodes in black box.
            b_box_nodes = find_nodes_in_b_box(bin_num_rep)
            # Remember that each node is visited only once so omit cases when it is not true.
            if k not in b_box_nodes:
                distance = 0
                if len(b_box_nodes) == 0:
                    distance = count_distance_cost(0, k-1, graph=graph)
                else:
                    distance, path = count_complex_distance_cost(0, b_box_nodes, k-1, graph=graph)
                    if (len(b_box_nodes) == (l-1)) and (shortest_path["path_cost"] > distance + graph[k-1][0]):
                        shortest_path["path_cost"] = distance + graph[k-1][0]
                        shortest_path["nodes"] = [1, path, k]
                print(1, "->", b_box_nodes, "->", k, "cost: ", distance)
    print("Shortest distance (Hamilton's cycle):\n", "Path: ", shortest_path["nodes"], ", Cost: ", shortest_path["path_cost"] )

