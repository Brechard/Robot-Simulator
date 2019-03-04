"""
This file exists so that we can code different kinds of crossovers and experiment with them
"""
import random

import numpy as np


def one_point_crossover(parent_1, parent_2):
    """ Generate the 2 possible single point products and pick a random one """
    point = random.randint(0, len(parent_1))
    p1 = parent_1[:point] + parent_2[point:]  # possibility 1
    p2 = parent_2[:point] + parent_1[point:]  # possibility 2
    offspring = [p1, p2]
    return offspring[random.randrange(0,2)]  # Return a random possibility


def mutation_v1(genome, mutation_prob = 0.05, limit = 1):
    """ Apply a hard mutation using the mutation rate and the value limits """
    for i in range(0, len(genome)):
        if mutation_prob > random.random():
            genome[i] = random.uniform(-limit, limit)
    return genome
