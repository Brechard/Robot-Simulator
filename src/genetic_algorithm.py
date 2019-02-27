import random
import numpy as np

from src.gui import GFX
from src.neuralnet import *
import crossover_mutation
from src.wall import Wall
from src.robot import Robot

# Build the invironment for a robot
WIDTH = 1040
HEIGHT = 700
SCALE = 50
vertical_step = HEIGHT / SCALE
horizontal_step = WIDTH / SCALE
vertical_bins = np.linspace(0, HEIGHT, num = SCALE)
horizontal_bins = np.linspace(0, WIDTH, num = SCALE)

# Build the walls
wall_list = []
padding = 20
wall_list.append(Wall((padding, padding), (WIDTH - padding, padding)))
wall_list.append(Wall((padding, HEIGHT - padding), (WIDTH - padding, HEIGHT - padding)))
wall_list.append(Wall((padding, padding), (padding, HEIGHT - padding)))
wall_list.append(Wall((WIDTH - padding, padding), (WIDTH - padding, HEIGHT - padding)))
padding = 230
wall_list.append(Wall((padding * 2, padding), (WIDTH - padding, padding)))
wall_list.append(Wall((padding, HEIGHT - padding), (WIDTH - padding, HEIGHT - padding)))
wall_list.append(Wall((padding * 2, padding), (padding, HEIGHT - padding)))
wall_list.append(Wall((WIDTH - padding, padding), (WIDTH - padding, HEIGHT - padding)))


def calculate_fitness(robot, times = 200):
    """
    Start the simulation of movement of a robot and calculate the fitness
    :param robot:
    :param times: how many times calculate update the fitness
    :return: fitness of the robot
    """
    visited = np.zeros((SCALE, SCALE))
    visited_arr = []
    x, y = robot.x, robot.y
    fitness = 0
    fitness_history = []

    # Start simulation of movement
    for i in range(times):
        old_x, old_y = x, y
        collided, x, y = robot.update_position()
        delta_fitness = 0

        x_bin_idx = np.digitize(x, horizontal_bins)
        y_bin_idx = np.digitize(y, vertical_bins)

        # Increase fitness calculated when new space visited
        if visited[x_bin_idx, y_bin_idx] == 0:
            visited[x_bin_idx, y_bin_idx] = 1
            visited_arr.append([x_bin_idx, y_bin_idx])
            delta_fitness += 1

        # Decrease fitness if wall collided
        if collided:
            delta_fitness -= 5

        # Decrease fitness if didnt move:
        if old_x == x and old_y == y:
            delta_fitness -= 1

        fitness_history.append(fitness)
        fitness += delta_fitness
    return fitness


def calculate_diversity(population):
    diversity = 0
    for i in (range(len(population))):
        for j in range(len(population)):
            if i != j:
                first_robot = population[i]
                second_robot = population[j]
                # for k in range(len(first_robot.nn.weights)):
                #     for l in range(len(first_robot.nn.weights[k])):
                #         diversity += abs(first_robot.nn.weights[k][l] - second_robot.nn.weights[k][l])

                result = np.absolute(np.array(first_robot.get_NN_weights())- np.array(second_robot.get_NN_weights()))
                print()


# def write_weights(n_generation, poulation):
    #TODO write down the weights in FILE
    """
    :param n_generation: 
    :param poulation: 
    :return: 
    """



def genetics(n_generation = 50, population_size = 50, n_selected = 5):
    population = []
    for r in range(population_size):
        """ Since we are starting the population, we don't send weights so that they are created randomly"""
        population.append(Robot(WIDTH, HEIGHT, wall_list))

    for generation in range(n_generation):
        fitness = np.array([calculate_fitness(robot) for robot in population])
        for robot in fitness:
            print(robot)
        best_idx = np.argpartition(fitness, -n_selected)[-n_selected:]
        best_robots = [population[idx] for idx in best_idx]
        new_population_weights = []
        for i in range(population_size):
            """ Call a crossover function that is going to return the new weights """
            random.shuffle(best_robots)
            parent_1, parent_2 = best_robots[:2]
            crossover = crossover_mutation.one_point_crossover(parent_1.get_NN_weights_flatten(), parent_2.get_NN_weights_flatten())
            mutation = crossover_mutation.mutation_v1(crossover)
            new_population_weights.append(mutation)

        print('\033[94m', "Best fitness in generation", generation, "is:", np.max(fitness),
              ", avg fitness:", np.mean(fitness), '\033[0m')

        population = []
        for r in range(population_size):
            population.append(Robot(WIDTH, HEIGHT, wall_list, weights = new_population_weights[r]))
        diversity = calculate_diversity(population)
        print('\033[94m', "The population diversity", generation, "is:", diversity)
    return population[np.argmax(fitness)]

best_robot = genetics()

gui = GFX()
gui.set_robot(best_robot)
gui.main(True, 10000)
