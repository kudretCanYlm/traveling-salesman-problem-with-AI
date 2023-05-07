import math

from aco import ACO, Graph
from plot import plot


def distance(city1: dict, city2: dict):
    return math.sqrt((city1['x'] - city2['x']) ** 2 + (city1['y'] - city2['y']) ** 2)


def main():
    points_x = [3639, 3569, 3904, 3506, 3237, 3089, 3238, 4172, 4020, 4095, 3007, 2562, 2788, 2381, 1332,
                3715, 3918, 4061, 3780, 3676, 4029, 4263, 3429, 3507, 3394, 3439, 2935, 3140, 2545, 2778, 2370]
    points_y = [1315, 1438, 1289, 1221, 1764, 1251, 1229, 1125, 1142, 626, 1970, 1756, 1491, 1676, 695,
                1678, 2179, 2370, 2212, 2578, 2838, 2931, 1908, 2367, 2643, 3201, 3240, 3550, 2357, 2826, 2975]

    cities = []
    points = []
    point_len = points_x.__len__()

    for i in range(point_len):
        cities.append(dict(index=int(i), x=int(
            points_x[i]), y=int(points_y[i])))
        points.append((int(points_x[i]), int(points_y[i])))

    cost_matrix = []
    rank = len(cities)
    for i in range(rank):
        row = []
        for j in range(rank):
            row.append(distance(cities[i], cities[j]))
        cost_matrix.append(row)
    aco = ACO(10, 100, 1.0, 10.0, 0.5, 10, 2)
    graph = Graph(cost_matrix, rank)
    path, cost = aco.solve(graph)
    print('cost: {}, path: {}'.format(cost, path))
    plot(points, path)


if __name__ == '__main__':
    main()
