import operator

import matplotlib.pyplot as plt


def plot(points, path: list):
    x = []
    y = []

    for point in points:
        x.append(point[0])
        y.append(point[1])

    # noinspection PyUnusedLocal
    y = list(map(operator.sub, [max(y) for i in range(len(points))], y))
    plt.plot(x, y, 'co')

    for _ in range(1, len(path)):

        i = path[_ - 1]
        j = path[_]
        # noinspection PyUnresolvedReferences
        plt.arrow(x[i], y[i], x[j] - x[i], y[j] - y[i],
                  color='r', length_includes_head=True)

    for i in range(x.__len__()):
        plt.text(x[i], y[i], str(i), fontsize=16,
                 bbox=dict(facecolor='red', alpha=1))

    plt.text((max(x) * 1.1)/5, (max(y) * 1.1)/5, "path: "+str(path))

    # noinspection PyTypeChecker
    plt.xlim(0, max(x) * 1.1)
    # noinspection PyTypeChecker
    plt.ylim(0, max(y) * 1.1)
    plt.show()
