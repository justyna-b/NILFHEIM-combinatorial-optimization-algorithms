import copy
import time

def generate_input(size):
    input_data = [2]
    for i in range(size):
        input_data.append(input_data[i-1]*2)
    return input_data

L = generate_input(22)

epsilon = 0.5
t = 16000
L = sorted(L)

def trim(l, delta):
    # Remove gamma-approximate elements.
    l_out = [l[0]]
    tmp = l[0]
    for i in range(1, len(l)):
        if (tmp < (1 - delta) * l[i]):
            l_out.append(l[i])
            tmp = l[i]
    return l_out

def scal(l, x):
    # Merge, sort and remove duplicates.
    left = copy.deepcopy(l)
    res = []
    right = list(map(lambda v: v + x, left))

    idx_l = 0
    idx_r = 0

    while idx_l < len(left) and idx_r < len(right):

        if left[idx_l] < right[idx_r]:
            res.append(left[idx_l])
            idx_l += 1
        elif (left[idx_l] > right[idx_r]):
            res.append(right[idx_r])
            idx_r += 1
        elif (left[idx_l] == right[idx_r]):
            res.append(left[idx_l])
            idx_r += 1
            idx_l += 1

    return res + right[idx_r:]

def subset_sum_fptas(epsilon, l, t):
    delta = epsilon/len(l)
    l_res = [0]
    for i in range(len(L)):
        e_iter = scal(l_res, l[i])
        l_iter = trim(e_iter, delta)
        l_res = [s for s in l_iter if s <= t]
    return l_res[-1]

start = round(time.time()*1000)
print(subset_sum_fptas(epsilon, L,t))
end = round(time.time()*1000)
print(f'Proceeding time {end - start}')
