import random

import crossover_mutation
from src.gui import GFX
from src.neuralnet import *
from src.robot import Robot
from src.wall import Wall

# Build the invironment for a robot
WIDTH = 1040
HEIGHT = 700
SCALE = 50
vertical_bins = np.linspace(0, HEIGHT, num=SCALE)
horizontal_bins = np.linspace(0, WIDTH, num=SCALE)

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


def load_weights():
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


def save_weights(population):
    """
    Save the weights of all the population
    :param population: Array that contains  all the robots of the population to save
    """
    weights = []
    for robot in population:
        weights.append(robot.get_NN_weights_flatten())
    weights = np.array(weights)
    np.savetxt("weights.txt", weights, fmt='%d')
    print("Weights saved")


def run_robot_simulation(robot, times=1000):
    """
    Start the simulation of movement of a robot and calculate the fitness
    :param robot:
    :param times: how many times calculate update the fitness
    :return: fitness of the robot
    """

    # Start simulation of movement
    for i in range(times):
        robot.update_position()

    return robot.fitness


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

                result = np.absolute(first_robot.get_NN_weights() - second_robot.get_NN_weights())
                res = 0
                for row in result:
                    for column in row:
                        for smth in column:
                            res += smth
                return res


def genetics(n_generation=20, population_size=100, n_selected=5, population=[]):
    for r in range(population_size):
        """ Since we are starting the population, we don't send weights so that they are created randomly"""
        population.append(Robot(WIDTH, HEIGHT, wall_list))

    for generation in range(n_generation):
        fitness = np.array([run_robot_simulation(robot) for robot in population])
        for robot in fitness:
            print(robot)
        best_idx = np.argpartition(fitness, -n_selected)[-n_selected:]
        best_robots = [population[idx] for idx in best_idx]
        new_population_weights = []
        for i in range(population_size):
            """ Call a crossover function that is going to return the new weights """
            random.shuffle(best_robots)
            parent_1, parent_2 = best_robots[:2]
            crossover = crossover_mutation.one_point_crossover(parent_1.get_NN_weights_flatten(),
                                                               parent_2.get_NN_weights_flatten())
            mutation = crossover_mutation.mutation_v1(crossover)
            new_population_weights.append(mutation)

        print('\033[94m', "Best fitness in generation", generation, "is:", np.max(fitness),
              ", avg fitness:", np.mean(fitness), '\033[0m')

        population = []
        for r in range(population_size):
            population.append(Robot(WIDTH, HEIGHT, wall_list, weights=new_population_weights[r]))
        diversity = calculate_diversity(population)
        print('\033[94m', "The population diversity", generation, "is:", diversity, '\033[0m')
        save_weights(population)

    return population[np.argmax(fitness)]


# load_weights()
# best_robot = genetics(population=load_weights())

gui = GFX()
gui.set_robot(Robot(WIDTH, HEIGHT, wall_list))
gui.main(True, 10000)
