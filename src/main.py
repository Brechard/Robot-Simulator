import numpy as np
import os
import datetime
from src.robot import Robot

DIR = 'weights/'+ datetime.datetime.now().strftime("%m%d_%H%M%S")

def init_dir(i):
    dir=os.path.dirname(DIR+'/gen'+str(i)+'/w')
    if not os.path.exists(dir):
        print('Saving weights in directory: ', DIR)
        os.makedirs(DIR+'/gen'+str(i))

def load_population(WIDTH, HEIGHT, wall_list, path):
    """
    Load the weights of the population
    @return population: array of robots
    """
    weights = np.loadtxt(path+'/weights.txt', dtype=int)
    population = []
    for r_weights in weights:
        population.append(Robot(WIDTH, HEIGHT, wall_list, r_weights))
    print("Weights loaded")
    return population


def save_population(population,i):
    """
    Save the weights of all the population
    :param population: Array that contains  all the robots of the population to save
    """
    weights = []
    for robot in population:
        weights.append(robot.get_NN_weights_flatten())

    weights = np.array(weights)
    init_dir(i)
    np.savetxt(DIR+"/gen"+str(i)+"/weights.txt", weights)
    print("Population weights saved")


def save_best_robot(robot, i):
    init_dir(i)
    np.savetxt(DIR+"/gen"+str(i)+"/best_robot.txt", robot.get_NN_weights_flatten())


def load_best_weights(dir):
    """ Return the weights of the best robot of the population """
    return np.loadtxt(dir+'/best_robot.txt', dtype=float)
