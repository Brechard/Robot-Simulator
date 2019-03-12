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
    return offspring[random.randrange(0, len(offspring))]  # Return a random possibility


def two_point_crossover(parent_1, parent_2):
    length = len(parent_1)
    point1 = random.randrange(0, int(length - 1 * 0.65))
    point2 = random.randrange(point1, length - 1)
    parent_1partA = parent_1[0:point1]
    parent_1partB = parent_1[point1:point2]
    parent_1partC = parent_1[point2:]
    parent_2partA = parent_2[0:point1]
    parent_2partB = parent_2[point1:point2]
    parent_2partC = parent_2[point2:]

    # All posibilities of combining these 6 parts:
    offspring = [
        parent_1partA + parent_2partB + parent_1partC,
        parent_2partA + parent_1partB + parent_2partC,
        parent_2partA + parent_2partB + parent_1partC,
        parent_1partA + parent_1partB + parent_2partC,
        parent_2partA + parent_1partB + parent_1partC,
        parent_1partA + parent_2partB + parent_2partC]

    return offspring[random.randrange(0, len(offspring))]  # Return a random possibility


def mutation_v1(genome, mutation_prob = 0.05, limit = 1):
    """ Apply a hard mutation using the mutation rate and the value limits """
    for i in range(0, len(genome)):
        if mutation_prob > random.random():
            genome[i] = random.uniform(-limit, limit)
    return genome
