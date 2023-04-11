import math
from matplotlib import pyplot as plt
import time

def create(start_point, end_point, cross_points):
    points = []
    if (
        (len(cross_points) < 1) and
        (start_point[0] == end_point[0]) and
        (start_point[1] != end_point[1])):
        for y_i in range(end_point[1]):
            points.append((0, y_i))
    elif (len(cross_points)==3):
        for y_i in range(cross_points[0][1]):
            points.append((0, y_i))
        for x_i in range(cross_points[1][0]):
            points.append((x_i, cross_points[1][0]))
        for y_i in range(cross_points[2][0]):
            points.append((cross_points[2][0], cross_points[1][1]-y_i))
        for x_i in range(cross_points[2][0]):
            points.append((cross_points[2][0]-x_i, 0))
    elif (start_point[0]==end_point[0]):
        for y_i in range(end_point[1]):
            points.append((start_point[0], y_i))
    elif (start_point[1]==end_point[1]):
        for x_i in range(end_point[0]):
            points.append((x_i, end_point[1]))
    return points

def draw_points(points, point1, point2):
    xs, ys = zip(*points)
    xb, yb = zip(*[point1, point2])
    plt.figure()
    plt.scatter(xs,ys, marker='o', s=1)
    plt.scatter(xb, yb, marker='o', s=2, color="r" )
    plt.show()

#---- Sort points by x and by y values ----
def create_s(points):
    s_x = sorted(points, key = lambda x: x[0])
    s_y = sorted(points, key = lambda x: (x[1], x[0]))
    # print(f'S_x = {s_x} \nS_y = {s_y}')
    return s_x, s_y

def recursively_divide(x_sorted_points):
    mid = math.ceil(len(x_sorted_points)/2)
    #---- Points lower than l "straight line" ----
    l = x_sorted_points[:mid]
    #---- Points higher than l "straight line" ----
    r = x_sorted_points[mid:]

    if len(x_sorted_points) <= 3:
        p1, p2, delta_1 = count_distances(l + r)
        return list([delta_1, p1, p2])
    else:
        return recursively_divide(x_sorted_points[:mid]) + recursively_divide(x_sorted_points[mid:])

def count_distances(points):
    best_pair = (),()
    min_val = float('inf')
    for i in range(len(points)-1):
        for j in range(i+1, len(points)):
            current_distance = count_euclidean_distance(points[i], points[j])
            if current_distance < min_val:
                min_val = current_distance
                best_pair = points[i], points[j]
    return [best_pair[0], best_pair[1], min_val]

def count_euclidean_distance(point_a, point_b):
    #---- Euclidean distance ----
    return math.sqrt((point_b[0]-point_a[0])**2 + (point_b[1]-point_a[1])**2)

def choose_winner(s_y_step_3, delta_1):
    best_delta = delta_1
    best_pair = []
    for i in range(len(s_y_step_3) - 1):
        for j in range(i+1, min(i+6, len(s_y_step_3))):
            p, q = s_y_step_3[i], s_y_step_3[j]
            dst = count_euclidean_distance(p,q)
            if dst < best_delta:
                best_pair = p, q
                best_delta = dst
    return best_pair, best_delta



if __name__ == "__main__":

    points = create((0,0), (0,524288), cross_points=[])

    start = time.process_time()
    #---- 1. A) Sort by X and by Y ----
    x_sorted, y_sorted = create_s(points)
    #---- 1. B) take medium point from array, last point from S1 ----
    l_x = x_sorted[math.ceil(len(x_sorted)/2)-1][0]

    #---- S1 and S2 ----
    s1_y, s2_y = y_sorted[:math.ceil(len(y_sorted)/2)], y_sorted[math.ceil(len(y_sorted)/2):]

    #---- 2. A) Recursively resolve S1/S2 problem ----
    points_t = recursively_divide(x_sorted)

    #---- 2. B) Set delta ----
    delta_1, p1, p2 = points_t[0], points_t[1], points_t[2]
    i = 0
    for packet in range(0, len(points_t), 3):
        if points_t[i] < delta_1:
            delta_1 = points_t[i]
            p1 = points_t[i+1]
            p2 = points_t[i+2]
        i+=3

    #---- Filter points in +/- delta area ----
    s_y_step_3 = list(filter(lambda point: point[0] <= abs(l_x-delta_1), y_sorted))

    closest_pair, delta_3 = choose_winner(s_y_step_3, delta_1)

    end = time.process_time()

    besties, delta = None, None
    try:
        print(f'Closest pair of points in given set:\nA={closest_pair[0]} B={closest_pair[1]} Distance={delta_3}')
        besties, delta = closest_pair, delta_3
    except:
        print(f'Closest pair of points in given set:\nA={p1} B={p2} Distance={delta_1}')
        besties, delta = [p1, p2], delta_1

    print(f'Total time: {end - start}')

    draw_points(points, besties[0], besties[1])
