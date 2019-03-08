import random

from matplotlib import pyplot as plt

import crossover_mutation
import main
# from src.wall import Wall
import rooms
from src.gui import GFX
from src.neuralnet import *
from src.robot import Robot

NUM_THREADS = 10
# NUM_THREADS = 1  # Set to 1 to disable multiprocessing

# Build the environment for a robot
WIDTH = 840
HEIGHT = 600
# WIDTH = 500
# HEIGHT = 350

# Build the walls
wall_list = rooms.room_1


def run_robot_simulation(params):
	"""
	Start the simulation of movement of a robot and calculate the fitness using multiple initial positions
	:params 0 robot: Robot object
	:params 1 times: how many times calculate update the fitness
	:params 2 draw: T/F enable GFX
	:return: fitness of the robot
	"""
	robot = params[0]
	times = params[1]
	draw = params[2]
	wall_list = params[3]
	# initial_positions = [(100, 150, 0), (WIDTH - 100, 150, 30), (100, HEIGHT - 150, 145)]
	initial_positions = [(100, 150, 0)]
	fitness = 0
	for j in range(len(initial_positions)):
		# Start simulation of movement
		bot = Robot(WIDTH, HEIGHT, wall_list, weights=robot.get_NN_weights_flatten())
		bot.set_pos(initial_positions[j][0], initial_positions[j][1], initial_positions[j][2])
		if not draw:
			for i in range(times):
				bot.update_position()

				# If robot is stuck, terminate the simulation
				if bot.n_not_moved > 50:
					bot.fitness = -100
					break
		else:
			gui = GFX(wall_list=wall_list)
			gui.set_robot(bot)
			gui.main(True, max_time=times, kill_when_stuck=True)
		fitness += bot.fitness
	return fitness


def calculate_diversity(population):
	""" Sum of Euclidean distances """
	diversity = 0
	for i in (range(len(population))):
		for j in range(len(population)):
			if i != j:
				a = np.asarray(population[i].get_NN_weights_flatten())
				b = np.asarray(population[j].get_NN_weights_flatten())
				diversity += np.linalg.norm(a - b)
	return diversity


def get_best_individual(path):
	return Robot(WIDTH, HEIGHT, wall_list, main.load_best_weights(path))


def genetics(n_generation=6, population_size=30, n_selected=5, simulation_steps=500,
			 mutation_rate=0.05, elitism=0.1, robot_rooms=[rooms.room_1, rooms.room_2, rooms.room_3],
			 load_population='', draw=False):
	if load_population != '':
		population = main.load_population(WIDTH, HEIGHT, wall_list, load_population)
	else:
		population = []
		for r in range(population_size):
			""" Since we are starting the population, we don't send weights so that they are created randomly"""
			population.append(Robot(WIDTH, HEIGHT, wall_list))
		print("Initialized random population. size: ", population_size)

	stats = []
	multiprocessing = False
	if not draw and NUM_THREADS > 1:
		from multiprocessing import Pool as ThreadPool
		pool = ThreadPool(NUM_THREADS)
		multiprocessing = True
	for generation in range(n_generation):
		# Simulate fitness for each individual
		fitness = np.zeros((len(robot_rooms), population_size))
		for i, room in enumerate(robot_rooms):
			# Execute every robot in every room
			if not multiprocessing:
				fitness[i] = np.array(
					[run_robot_simulation([robot, simulation_steps, draw, room]) for robot in population])
				for pos, robot in enumerate(fitness):
					print("Robot", pos, "fitness:", robot)
			else:
				# Use the thread pool
				inputs = []
				for j, robot in enumerate(population):
					inputs.append([robot, simulation_steps, False, room])
				fitness[i] = pool.map(run_robot_simulation, inputs)

		# The final fitness of each robot is the average fitness achieved in the different rooms
		fitness = [np.average(fitness[:, robot]) for robot in range(population_size)]

		# Reproduce
		best_idx = (-np.array(fitness)).argsort()[:n_selected]
		best_robots = [population[idx] for idx in best_idx]
		new_population_weights = []
		num_offspring = int(population_size * (1 - elitism))
		for i in range(num_offspring):
			""" Call a crossover function that is going to return the new weights """
			# crossover between 2 random parents
			random.shuffle(best_robots)
			parent_1, parent_2 = best_robots[:2]
			crossover = crossover_mutation.two_point_crossover(parent_1.get_NN_weights_flatten(),
															   parent_2.get_NN_weights_flatten())

			# Mutation
			mutation = crossover_mutation.mutation_v1(crossover, mutation_rate, 5)
			new_population_weights.append(mutation)

		# Elitism: Add the best performing individuals to the new population without crossover but with mutation
		for i in range(population_size - num_offspring):
			genome = population[best_idx[i]].get_NN_weights_flatten()
			new_population_weights.append(crossover_mutation.mutation_v1(genome, mutation_rate, 5))

		# Stats
		max_fitness = np.max(fitness)
		avg_fitness = np.mean(fitness)
		print('\033[94m', "Best fitness in generation", generation, "is:", max_fitness,
			  ", avg fitness:", avg_fitness, '\033[0m')
		diversity = calculate_diversity(population)
		print('\033[94m', "The population diversity", generation, "is:", diversity, '\033[0m')
		stats.append([generation, np.max(fitness), np.mean(fitness), diversity])

		# Save
		main.save_population(population, generation)
		main.save_best_robot(population[np.argmax(fitness)], generation)

		# Build new population using the new weights
		population = []
		for r in range(population_size):
			population.append(Robot(WIDTH, HEIGHT, wall_list, weights=new_population_weights[r]))

		if generation > 0 and generation % 5 == 0 or generation == n_generation - 1:
			fig, ax1 = plt.subplots()
			ax1.plot(np.array(stats)[:, 1], '-r', label='max fitness')
			ax1.plot(np.array(stats)[:, 2], '--r', label='avg fitness')
			ax1.set_xlabel('Generation')
			ax1.set_ylabel('Fitness', color='r')
			ax1.tick_params('y', colors='r')

			ax2 = ax1.twinx()
			ax2.plot(np.array(stats)[:, 3], '-b', label='diversity')
			ax2.set_ylabel('Diversity', color='b')

			fig.legend()
			fig.tight_layout()
			plt.show()

	return population[np.argmax(fitness)]
