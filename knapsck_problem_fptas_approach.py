import math
import time

def find_res(matrix, udzwig):
    filtered = [possibility for possibility in matrix[-1] if possibility <= udzwig]
    return (max(filtered))

def knapsack(items, V, values, weights):
    res = [[0 for x in range(V+1)] for x in range(items)]
    for i in range(items):
        for v in range(V+1):
            if (v == 0) :
                res[i][v] = 1
            if (i == 0) and (v != 0) and values[i] == v:
                res[i][v] = weights[i]
            elif (i == 0) and (v != 0) and values[i] != v:
                res[i][v] = math.inf
            elif (i >= 1) and (v >= values[i]):
                res[i][v] = min(res[i-1][v], res[i-1][v-values[i]]+weights[i])
            else:
                res[i][v] = res[i-1][v]

    print(find_res(res, max_weight))

def generate_input(size):
    input_data = [2]
    for i in range(size):
        input_data.append(input_data[i-1]*2)
    return input_data

values = generate_input(22)
weights = generate_input(22)
V = sum(values)
max_weight = 500000

# Constant epsilon value, allowable margin of error.
EPSILON = 0.5
P = max([item for item in values])
K = (EPSILON * P)/len(values)
k_mod_vlues = []
for item in values:
    k_mod_vlues.append(math.floor(K * item))

start = round(time.time()*1000)
knapsack(len(values), V, values, weights)
end = round(time.time()*1000)
print(f'Proceeding time: {end - start}')

