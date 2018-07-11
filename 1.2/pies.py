"""
tree:
    circle  -> increase diameter
            -> decrease diameter
            -> jump to closest & radius with max score (search linearly)

increase radius while success rate grows
when 
"""

# tuple = (x, y, True, radius)
visited_states = []
current_state = []

def dist_sq(a, b):
    return (a[0] - b[0])**2 + (a[1] - b[1])**2

# success rate - how many points are classified correctly, in %
def eval_func(data, point):
    min_x = point[0] - point[3]
    max_x = point[0] + point[3]

    correct = 0
    in_circle = 0

    for i in range(0, len(data)):
        if dist_sq(data[i], point) > point[3] ** 2:
            if data[i][2] == False:
                correct += 1
        else:
            in_circle += 1
            if data[i][2] == True:
                correct += 1

    return correct / len(data)
    
def get_random_positive_example(data):
    import random
    point = random.choice([p for p in data if p[2]])

    return point

def get_closest_not_visited_point(data, point):
    import random
    minp, mind = point, 20000

    for p in data:
        if p == point:
            continue
        d = dist_sq(p, point)

        if (d < mind) or (d == mind and random.randint(0, 100) < 50):
            if p not in data:
                minp, mind = p, d

def increase_radius(data, point):
    suc = eval_func(data, point)

    while point[3] < 100:
        point[3] += 1

        ef = eval_func(data, point)
        
        if ef < suc:
            point[3] -= 1
            return ef

        if ef > suc:
            suc = ef
    return suc

def decrease_radius(data, point):
    suc = eval_func(data, point)

    while point[3] > 0:
        point[3] -= 1

        ef = eval_func(data, point)

        if ef < suc:
            point[3] += 1
            return ef
        
        if ef > suc:
            suc = ef
    return suc

def hill_climbing(data):
    global current_state
    global visited_states

    current_state = get_random_positive_example(data)
    current_state.append(0)
    visited_states.append(current_state)

    #print(current_state, eval_func(data, current_state))
    #print(current_state, increase_radius(data, current_state))

    #csi = data.index(current_state)
    best, bp = 0, None
    for p in data:
        m = list(p)
        m.append(0)
        score = increase_radius(data, m)
        if score > best:
            best, bp = score, m
    print('Best score has point {}: {}'.format(bp, best))
    return bp