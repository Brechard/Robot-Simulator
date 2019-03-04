import random

import crossover_mutation
from src.gui import GFX
from src.neuralnet import *
from src.robot import Robot
from src.wall import Wall
import main
from matplotlib import pyplot as plt

# Build the environment for a robot
WIDTH = 840
HEIGHT = 600
SCALE = 200
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
wall_list.append(Wall((padding, padding), (WIDTH - padding, padding)))
wall_list.append(Wall((padding, HEIGHT - padding), (WIDTH - padding, HEIGHT - padding)))
wall_list.append(Wall((padding, padding), (padding, HEIGHT - padding)))
wall_list.append(Wall((WIDTH - padding, padding), (WIDTH - padding, HEIGHT - padding)))

# wall_list.append(Wall((padding * 2, padding), (WIDTH - padding, padding)))
# wall_list.append(Wall((padding, HEIGHT - padding), (WIDTH - padding, HEIGHT - padding)))
# wall_list.append(Wall((padding * 2, padding), (padding, HEIGHT - padding)))
# wall_list.append(Wall((WIDTH - padding, padding), (WIDTH - padding, HEIGHT - padding)))


def run_robot_simulation(robot, times=100):
	"""
    Start the simulation of movement of a robot and calculate the fitness using multiple initial positions
    :param robot:
    :param times: how many times calculate update the fitness
    :return: fitness of the robot
    """
	initial_positions = [(100, 150, 0), (WIDTH - 100, 150, 30), (100, HEIGHT - 150, 145)]
	# initial_positions = [(100, 150, 0)]
	fitness = 0
	for j in range(len(initial_positions)):
		# Start simulation of movement
		bot = Robot(WIDTH, HEIGHT, wall_list, weights=robot.get_NN_weights_flatten())
		bot.set_pos(initial_positions[j][0], initial_positions[j][1], initial_positions[j][2])
		for i in range(times):
			bot.update_position()
		fitness += bot.fitness
	return fitness


def calculate_diversity(population):
	# TODO Check this method
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


def get_best_individual():
	return Robot(WIDTH, HEIGHT, wall_list, main.load_best_weights())


def genetics(n_generation=6, population_size=30, n_selected=5, mutation_rate=0.05, elitism=0.1, load_population=False):
	if load_population:
		population = main.load_population(WIDTH, HEIGHT, wall_list)
	else:
		population = []
		for r in range(population_size):
			""" Since we are starting the population, we don't send weights so that they are created randomly"""
			population.append(Robot(WIDTH, HEIGHT, wall_list))

	stats = []
	for generation in range(n_generation):
		# Simulate fitness for each individual
		fitness = np.array([run_robot_simulation(robot, times=450) for robot in population])
		for pos, robot in enumerate(fitness):
			print("Robot", pos, "fitness:", robot)

		# Reproduce
		best_idx = np.argpartition(fitness, -n_selected)[-n_selected:]
		best_robots = [population[idx] for idx in best_idx]
		new_population_weights = []
		num_offspring = int(population_size*(1-elitism))
		for i in range(num_offspring):
			""" Call a crossover function that is going to return the new weights """
			# crossover between 2 random parents
			random.shuffle(best_robots)
			parent_1, parent_2 = best_robots[:2]
			crossover = crossover_mutation.one_point_crossover(parent_1.get_NN_weights_flatten(),
															   parent_2.get_NN_weights_flatten())

			# Mutation
			mutation = crossover_mutation.mutation_v1(crossover, mutation_rate, 5)
			new_population_weights.append(mutation)

		# Elitism: Add the best performing individuals to the new population without crossover but with mutation
		for i in range(population_size-num_offspring):
			genome = population[best_idx[i]].get_NN_weights_flatten()
			new_population_weights.append(crossover_mutation.mutation_v1(genome, mutation_rate, 5))

		print('\033[94m', "Best fitness in generation", generation, "is:", np.max(fitness),
			  ", avg fitness:", np.mean(fitness), '\033[0m')

		population = []
		for r in range(population_size):
			population.append(Robot(WIDTH, HEIGHT, wall_list, weights=new_population_weights[r]))
		diversity = calculate_diversity(population)
		stats.append([generation, np.max(fitness), np.mean(fitness), diversity])
		print('\033[94m', "The population diversity", generation, "is:", diversity, '\033[0m')
		main.save_population(population)
		main.save_best_robot(population[np.argmax(fitness)])

		if generation > 0:
			plt.figure()
			plt.plot(np.array(stats)[:,1], '-r', label='max fitness')
			plt.plot(np.array(stats)[:,2], '-b', label='avg fitness')
			plt.legend()
			plt.show()

	return population[np.argmax(fitness)]
