import math
from collections import defaultdict
import random
import time

# Prepare input data.
def prepare_input(x_range, y_range, set_size):
    base = (random.sample([(x, y) for x in range(x_range) for y in range(y_range)], set_size))
    lex = list(sorted(base))
    rev_lex = lex[::-1]
    shuffle = random.shuffle(base)
    return base, lex, rev_lex, shuffle

def brute_force_kmeans(points, ordering_type):
    start = time.time()*1000
    best = [math.inf, None, None]
    for idx in range(len(points)):
        for idx_p2 in range(len(points)):
            if points[idx] != points[idx_p2]:
                tmp = count_distance(points[idx], points[idx_p2])
                if tmp < best[0]:
                    best[0] = tmp
                    best[1] = points[idx]
                    best[2] = points[idx_p2]
    end = time.time()*1000
    print(f'{"*"*15}BRUTE FORCE ALGORITHM ({ordering_type}){"*"*15}')
    print(F'best pair: {(best[1], best[2])}, distance: {best[0]}')
    print(f'time: {end - start} \n')


def count_distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def count_point_star(point, delta):
    x = point[0]
    y = point[1]
    return ((math.floor(x/delta))*x, (math.floor(y/delta))*y)

def count_index(point, delta):
    x = point[0]
    y = point[1]
    return (math.floor(x/delta), math.floor(y/delta))

# Create grid for current delta, P i Q.
def create_grid(delta, p, q):
    p_prim = count_point_star(p, delta)
    q_prim = count_point_star(q, delta)
    p_prim_idx = count_index(p_prim, delta)
    q_prim_idx = count_index(q_prim, delta)
    s_prim = defaultdict(list)
    s_prim[p_prim_idx].append(p)
    s_prim[q_prim_idx].append(q)
    return s_prim

def find_smallest_distance_in_grid(grid, n_idxs, master_point):
    smallest = {"distance": math.inf, "points": (None, None)}
    counter = 0
    for idx in n_idxs:
        try:
            for p2 in grid[idx]:
                counter += 1
                if master_point != p2:
                    iter_dist = count_distance(master_point, p2)
                    if smallest["distance"] > iter_dist:
                        smallest["distance"] = iter_dist
                        smallest["points"] = (master_point, p2)
        except KeyError:
            continue
    return smallest

def support(points_l, delta, point):
    s_prim = defaultdict(list)
    points = points_l[:point]
    for point in points:
        point_2 = count_point_star(point, delta)
        index = count_index(point_2, delta)
        s_prim[index].append(point)
    return s_prim

def closest_pair(points_set):
    start = time.time()*1000
    p = points_set[0]
    q = points_set[1]

    # Initialize delta.
    delta = count_distance(p, q)

    # Initialize grid.
    p_q_grid = create_grid(delta, p, q)

    for i in range(2, len(points_set)):
        master = points_set[i]
        g_master = count_point_star(master, delta)
        curr_idx = count_index(g_master, delta)
        indexes = [(curr_idx[0]+1, curr_idx[1]),
            (curr_idx[0], curr_idx[1]+1),
            (curr_idx[0]+1, curr_idx[1]+1),
            (curr_idx[0]-1, curr_idx[1]),
            (curr_idx[0], curr_idx[1]-1),
            (curr_idx[0]-1, curr_idx[1]-1),
            (curr_idx[0]+1, curr_idx[1]-1),
            (curr_idx[0]-1, curr_idx[1]+1),
            (curr_idx[0], curr_idx[1])
            ]

        smallest_in_grid = find_smallest_distance_in_grid(p_q_grid, indexes, master)

        # Negative case.
        if smallest_in_grid["distance"] < delta:
            # Update P and Q.
            p = smallest_in_grid["points"][0]
            q = smallest_in_grid["points"][1]
            delta = smallest_in_grid["distance"]
            p_q_grid = defaultdict(list)
            p_q_grid = support(points_set, delta, i)
        else:
            # Positive case.
            # Expand grid with curren P and Q.
            grid = defaultdict(list, p_q_grid)
            grid[curr_idx].append(points_set[i])

    end = time.time()*1000
    return p, q, delta, (end - start)


if __name__ == "__main__":

    lex = random.shuffle([(1,1), (2,2), (4,4), (8,8), (16,16), (32,32), (64,64), (128,128)])
    print(lex)

    # Closest points algorithm.
    print(f'{"*"*15}CLOSEST ALGORITHM (lexicographic order){"*"*15}')
    p, q, distance, exe_time = closest_pair(lex)
    print(F'best pair: {(p, q)}, distance: {distance}')
    print(f'time: {exe_time}')

    # Brute force approach for comparison.
    brute_force_kmeans(lex, "lexicographic order")
