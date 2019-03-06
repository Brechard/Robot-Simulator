import random

import crossover_mutation
from src.gui import GFX
from src.neuralnet import *
from src.robot import Robot
from src.wall import Wall
import main
from matplotlib import pyplot as plt

NUM_THREADS = 10
# NUM_THREADS = 1  # Set to 1 to disable multiprocessing
if NUM_THREADS > 1:
	from multiprocessing import Pool as ThreadPool

# Build the environment for a robot
WIDTH = 840
HEIGHT = 600
# WIDTH = 500
# HEIGHT = 350

# Build the walls
wall_list = []
padding = 20
wall_list.append(Wall((padding, padding), (WIDTH - padding, padding)))
wall_list.append(Wall((padding, HEIGHT - padding), (WIDTH - padding, HEIGHT - padding)))
wall_list.append(Wall((padding, padding), (padding, HEIGHT - padding)))
wall_list.append(Wall((WIDTH - padding, padding), (WIDTH - padding, HEIGHT - padding)))

# padding = 230
# wall_list.append(Wall((padding, padding), (WIDTH - padding, padding)))
# wall_list.append(Wall((padding, HEIGHT - padding), (WIDTH - padding, HEIGHT - padding)))
# wall_list.append(Wall((padding, padding), (padding, HEIGHT - padding)))
# wall_list.append(Wall((WIDTH - padding, padding), (WIDTH - padding, HEIGHT - padding)))

# wall_list.append(Wall((padding * 2, padding), (WIDTH - padding, padding)))
# wall_list.append(Wall((padding, HEIGHT - padding), (WIDTH - padding, HEIGHT - padding)))
# wall_list.append(Wall((padding * 2, padding), (padding, HEIGHT - padding)))
# wall_list.append(Wall((WIDTH - padding, padding), (WIDTH - padding, HEIGHT - padding)))


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
	initial_positions = [(100, 150, 0), (WIDTH - 100, 150, 30), (100, HEIGHT - 150, 145)]
	# initial_positions = [(100, 150, 0)]
	fitness = 0
	for j in range(len(initial_positions)):
		# Start simulation of movement
		bot = Robot(WIDTH, HEIGHT, wall_list, weights=robot.get_NN_weights_flatten())
		bot.set_pos(initial_positions[j][0], initial_positions[j][1], initial_positions[j][2])
		if not draw:
			for i in range(times):
				bot.update_position()
		else:
			gui = GFX()
			gui.set_robot(bot)
			gui.main(True, times)
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
			 mutation_rate=0.05, elitism=0.1, load_population='', draw=False):
	if load_population != '':
		population = main.load_population(WIDTH, HEIGHT, wall_list, load_population)
	else:
		population = []
		for r in range(population_size):
			""" Since we are starting the population, we don't send weights so that they are created randomly"""
			population.append(Robot(WIDTH, HEIGHT, wall_list))
		print("Initialized random population. size: ", population_size)

	stats = []
	pool = ThreadPool(NUM_THREADS)
	for generation in range(n_generation):
		# Simulate fitness for each individual
		fitness = [None] * population_size
		if draw or NUM_THREADS <= 1:
			fitness = np.array([run_robot_simulation([robot, simulation_steps, draw]) for robot in population])
			for pos, robot in enumerate(fitness):
				print("Robot", pos, "fitness:", robot)
		else:
			# Use the thread pool
			inputs = []
			for i, robot in enumerate(population):
				inputs.append([robot, simulation_steps, False])
			fitness = pool.map(run_robot_simulation, inputs)

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
			crossover = crossover_mutation.two_point_crossover(parent_1.get_NN_weights_flatten(),
															   parent_2.get_NN_weights_flatten())

			# Mutation
			mutation = crossover_mutation.mutation_v1(crossover, mutation_rate, 5)
			new_population_weights.append(mutation)

		# Elitism: Add the best performing individuals to the new population without crossover but with mutation
		for i in range(population_size-num_offspring):
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

		if generation > 0:
			fig, ax1 = plt.subplots()
			ax1.plot(np.array(stats)[:,1], '-r', label='max fitness')
			ax1.plot(np.array(stats)[:,2], '--tomato', label='avg fitness')
			ax1.set_xlabel('Generation')
			ax1.set_ylabel('Fitness', color='r')
			ax1.tick_params('y', colors='r')

			ax2 = ax1.twinx()
			ax2.plot(np.array(stats)[:,3], '-k', label='diversity')
			ax2.set_ylabel('Diversity', color='k')

			fig.legend()
			fig.tight_layout()
			plt.show()

	return population[np.argmax(fitness)]
