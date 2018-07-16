"""
    k-NN classifier
"""

import operator
import random
import collections

import matplotlib.pyplot as plt
from math import sqrt, floor

def dist2(a, b):
    assert(len(a) == len(b)), '\na={}\nb={}'.format(a, b)

    return sum( map(lambda x: (x[0] - x[1])**2, list(zip(a, b))[:-1]) )

def dist(a, b):
    return sqrt(dist2(a, b))

def remove_redundant(dataset):
    pass

# point = (p1, p2, p3, ..., class)
def classify(dataset, k, point):

    distances = sorted(dataset, key=lambda x: dist2(x, point))
    classes = collections.defaultdict(int)

    for d in distances[0:k]:
        classes[d[-1]] += 1

    # return the class with most occurences
    c = max(classes.items(), key=operator.itemgetter(1))[0]
    return c

if __name__ == '__main__':
    import sys

    dataset = []
    filename = 'noise0'
    k = 1

    try:
        k = int(sys.argv[1])
        filename = sys.argv[2]
    except Exception as e:
        pass

    with open(filename, 'r') as dsf:
        dataset = [list(map(float, x.rstrip().split(','))) for x in dsf.readlines()]

    learning_set = [dataset[x] for x in random.sample(range(0, len(dataset)), floor(0.6*len(dataset)))]

    correct, wrong, total = 0, 0, 0
    for p in dataset:
        if p in learning_set:
            continue

        c = classify(learning_set, k, p)
        total += 1

        if c == p[-1]:
            correct += 1
        else:
            wrong += 1
    
    print('{}-NN success on test examples: {}'.format(k, correct / total))