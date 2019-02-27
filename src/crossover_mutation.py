"""
This file exists so that we can code different kinds of crossovers and experiment with them
"""
import random

import numpy as np


def one_point_crossover(parent_1, parent_2):
    point = random.randint(0, len(parent_1))
    return parent_1[:point] + parent_2[point:]


def mutation_v1(array, prob = 10):
    """ Probability should be out of 100 """

    limit = 0.5
    for pos in range(len(array)):
        seed = random.random() * 100
        if seed < prob:
            array[pos] = np.random.uniform(-limit, limit)
