import pies

# create pies dataset - everything where f(x) > y is too expensive
def create_pies_dataset(count, f):
    from random import randint

    output = []
    for i in range(0,count):
        (x, y) = (randint(0, 100), randint(0, 100))
        output.append( [x, y, f(x) >= y] )
    
    return output

if __name__ == '__main__':
    from math import log
    from matplotlib import pyplot as plt

    fun = lambda x: log(101-x) * 13
    dataset = create_pies_dataset(100, fun)
    dataset.sort(key=lambda x: x[1])
    dataset.sort(key=lambda x: x[0])
    
    bp = pies.hill_climbing(dataset)
    
    for p in dataset:
        if p[0] == bp[0] and p[1] == bp[1]:
            plt.plot(p[0], p[1], color='blue', marker='o')
        else:
            plt.plot(p[0], p[1], color=('green' if p[2] else 'red'), marker='o')

    circle = plt.Circle((bp[0],bp[1]), radius=bp[3], fill=False)
    ax=plt.gca()
    ax.add_patch(circle)
    plt.axis('scaled')
    
    plt.plot([fun(n) for n in range(0, 100)])
    plt.show()

