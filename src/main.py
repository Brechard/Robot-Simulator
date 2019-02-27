import random

from src.gui import GFX
from src.neuralnet import *
import crossover_mutation
from src.wall import Wall

WIDTH = 1040
HEIGHT = 700



def genetics(n_generation = 10, population_size = 10, n_selected = 3):
    population = []
    for r in range(population_size):
        """ Since we are starting the population, we don't send weights so that they are created randomly"""
        population.append(GFX())

    for generation in range(n_generation):
        fitness = np.array([gfx.main(False) for gfx in population])
        best_idx = np.argpartition(fitness, -n_selected)[-n_selected:]
        best_robots = [population[idx] for idx in best_idx]
        new_population_weights = []
        for i in range(population_size):
            """ Call a crossover function that is going to return the new weights """
            random.shuffle(best_robots)
            parent_1, parent_2 = best_robots[:2]
            crossover = crossover_mutation.one_point_crossover(parent_1.get_nn_weights(), parent_2.get_nn_weights())
            mutation = crossover_mutation.mutation_v1(crossover)
            new_population_weights.append(mutation)

        print('\033[94m', "Best fitness in generation", generation, "is:", np.max(fitness),
              ", avg fitness:", np.mean(fitness), '\033[0m')

        population = []
        for r in range(population_size):
            population.append(GFX(weights = new_population_weights[r]))

    return population[np.argmax(fitness)]


gui = genetics()
gui.main(True, 10000)
