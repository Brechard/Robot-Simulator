import datetime
import os

import numpy as np

DIR = 'weights/' + datetime.datetime.now().strftime("%m%d_%H%M%S")


def init_dir(i):
    dir = os.path.dirname(DIR + '/gen' + str(i) + '/w')
    if not os.path.exists(dir):
        print('Saving weights in directory: ', dir)
        os.makedirs(DIR + '/gen' + str(i))


def load_population(WIDTH, HEIGHT, wall_list, path):
    """
    Load the weights of the population
    @return population: array of robots
    """
    weights = np.loadtxt(path + '/weights.txt', dtype=float)
    population = []
    for r_weights in weights:
        population.append(Robot(WIDTH, HEIGHT, wall_list, r_weights))
    print("Previous population loaded as gen0: " + path)
    return population


def save_population(population, i):
    """
    Save the weights of all the population
    :param population: Array that contains  all the robots of the population to save
    """
    weights = []
    for robot in population:
        weights.append(robot.get_NN_weights_flatten())

    weights = np.array(weights)
    init_dir(i)
    np.savetxt(DIR + "/gen" + str(i) + "/weights.txt", weights)


def save_best_robot(robot, i):
    init_dir(i)
    np.savetxt(DIR + "/gen" + str(i) + "/best_robot.txt", robot.get_NN_weights_flatten())


def load_best_weights(dir):
    """ Return the weights of the best robot of the population """
    return np.loadtxt(dir + '/best_robot.txt', dtype=float)


import genetic_algorithm as g
from src.gui import GFX
from src.robot import Robot

import rooms


def main():
    n_generations = 50
    population_size = 50
    n_selected = 20
    elitism = 0.05
    simulation_steps = 5000
    draw = False

    mutation_rate = 0.02
    # robot_rooms = [rooms.room_1, rooms.room_2, rooms.room_3]
    # robot_rooms = [rooms.get_base_room(), rooms.room_2, rooms.room_3]
    robot_rooms = [rooms.room_2, rooms.room_3, rooms.room_5]
    # robot_rooms = [rooms.room_3]
    # robot_rooms = [rooms.room_4]
    # robot_rooms = [rooms.room_3]
    load_population_path = ''
    # load_population_path = 'weights/0309_163600/gen49' # Continues with a previous generation as gen0

    # best_robot = g.genetics(n_generation=n_generations, population_size=population_size, n_selected=n_selected,
    # 						elitism=elitism, simulation_steps=simulation_steps, robot_rooms=robot_rooms,
    # 						draw=draw, mutation_rate=mutation_rate, load_population=load_population_path)

    # best_robot = g.get_best_individual('weights/0309_005310/gen17')
    # best_robot = g.get_best_individual('weights/0309_005310/gen25')
    # best_robot = g.get_best_individual('weights/0309_124629/gen44')

    # best_robot = g.get_best_individual('weights_saved/0309_204413/gen49') # Empty room
    # best_robot = g.get_best_individual('weights/0309_204331/gen49') # Room3

    # best_robot = Robot(g.WIDTH, g.HEIGHT, rooms.room_3)
    gui = GFX()
    # gui.set_odometry_based_model()
    # best_robot.set_walls(rooms.get_base_room())
    # best_robot.set_walls(rooms.room_3)
    # best_robot.set_walls(rooms.room_5)
    # best_robot.set_pos(300, 450, 0)
    # best_robot.set_pos(600, 300, 0)
    # best_robot.set_pos(130, 150, 0)
    # best_robot.set_pos(100, g.HEIGHT - 150, 145)
    # gui.set_robot(best_robot)
    gui.main(draw=True, max_time=50000, kill_when_stuck=False)


if __name__ == "__main__":
    main()
