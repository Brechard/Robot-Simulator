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
	weights = np.loadtxt(path + '/weights.txt', dtype=int)
	population = []
	for r_weights in weights:
		population.append(Robot(WIDTH, HEIGHT, wall_list, r_weights))
	print("Weights loaded")
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


def main():
	# best_robot = g.genetics(load_population='weights/0304-194633', n_generation=1)

	best_robot = g.genetics(n_generation=30, population_size=30, n_selected=10, elitism=0.05, simulation_steps=500,
							draw=False)
	# best_robot = g.get_best_individual('weights/0306_222607/gen30')
	# best_robot = g.get_best_individual('weights/0307_185311/gen19')
	import rooms
	# best_robot = Robot(g.WIDTH, g.HEIGHT, rooms.room_1)
	gui = GFX()
	best_robot.set_pos(100, 150, 0)
	best_robot.set_walls(rooms.room_3)
	# best_robot.set_pos(genetic_algorithm.WIDTH-100,150, 30)
	# best_robot.set_pos(100, g.HEIGHT - 150, 145)
	gui.set_robot(best_robot)
	gui.main(True, 10000)


if __name__ == "__main__":
	main()
