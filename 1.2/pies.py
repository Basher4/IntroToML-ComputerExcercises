"""
tree:
    circle  -> increase diameter
            -> decrease diameter
            -> jump to closest & radius with max score (search linearly)
"""

# tuple = (x, y, True, radius)
visited_states = []
current_state = ()

def dist_sq(a, b):
    return (a[0] - b[0])**2 + (a[1] - b[1])**2

def eval_func(data):
    import bisect

    min_x = current_state[0] - current_state[3]
    max_x = current_state[0] + current_state[3]

    result = 0

    index = bisect.bisect_left(data, min_x)
    while (index < len(data) and data[index][0] < max_x):
        if data[index][2] == False:
            continue

        if dist_sq(data[index], current_state) <= current_state[2] ** 2:
            result += 1

        index += 1

    return result
    
def get_random_positive_example(data):
    import random
    point = random.choice([p for p in data if p[2]])

    return point

def get_closest_not_visited_point(data, point=current_state):
    i = data.index(point[:-1])

    d1 = dist_sq(point, data[i-1])
    d2 = dist_sq(point, data[i+1])

    return data[i-1] if d1 < d2 else d2

def hill_climbing(data):
    start = get_random_positive_example(data)
    current_state = start + (1,)
    visited_states.append(current_state)

