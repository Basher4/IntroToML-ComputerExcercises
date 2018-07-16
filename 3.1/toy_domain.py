import random

noise = [0, 5, 10, 15, 20, 25, 30, 40, 50, 60]
dataset = []

def figure(x, y):
    return (x - 0.5)**2 + (y - 0.5)**2 < 0.25 ** 2

for i in range(0, 1000):
    px, py = random.random(), random.random()
    fig = float(figure(px, py))

    if not [px, py, fig] in dataset:
        dataset.append([px, py, fig])

for n in noise:
    d = list(dataset)
    tochange = random.sample(range(0, len(dataset)), 100)

    for t in tochange:
        d[t][2] = 0.0 if d[t][2] else 1.0

    with open('noise{}'.format(n), 'w') as of:
        for l in d:
            of.write(','.join([str(x) for x in l]) + '\n')