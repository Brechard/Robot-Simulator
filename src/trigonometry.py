from scipy.optimize import minimize
import matplotlib.pyplot as plt
import numpy as np


def calculate_position_helper(distances, beacons):
    def error(x, c, r):
        return sum([(np.linalg.norm(x - c[i]) - r[i]) ** 2 for i in range(len(c))])
    beacons = np.array(beacons)

    l = len(beacons)
    s = sum(distances)
    # compute weight vector for initial guess
    w = [((l - 1) * s) / (s - w) for w in distances]
    # get initial guess of point location
    x0 = sum([w[i] * beacons[i] for i in range(l)])
    # optimize distance from signal origin to border of spheres
    return minimize(error, x0, args=(beacons, distances), method='Nelder-Mead').x


def calculate_position(distances, beacons):
    if len(beacons) < 3:
        return []

    return calculate_position_helper(distances, beacons)


def plot_and_calculate_position(angles, beacons):
    x = []
    y = []
    for point in beacons:
        x.append(point[0])
        y.append(point[1])

    plt.scatter(x, y)
    x, y = calculate_position(angles, beacons)
    plt.scatter(x, y)
    plt.show()
