import numpy as np

from src.robot import Robot


def load_population(WIDTH, HEIGHT, wall_list):
    """
    Load the weights of the population
    @return population: array of robots
    """
    weights = np.loadtxt('weights.txt', dtype=int)
    population = []
    for r_weights in weights:
        population.append(Robot(WIDTH, HEIGHT, wall_list, r_weights))
    print("Weights loaded")
    return population


def save_population(population):
    """
    Save the weights of all the population
    :param population: Array that contains  all the robots of the population to save
    """
    weights = []
    for robot in population:
        weights.append(robot.get_NN_weights_flatten())

    weights = np.array(weights)
    np.savetxt("weights.txt", weights)
    print("Population weights saved")


def save_best_robot(robot):
    np.savetxt("best_robot.txt", robot.get_NN_weights_flatten())


def load_best_weights():
    """ Return the weights of the best robot of the population """
    return np.loadtxt('best_robot.txt', dtype=float)
