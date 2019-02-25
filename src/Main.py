from src.gui import GFX
from src.neuralnet import *
import numpy as np
import random

# Test NN
nn = RNN(inputs=12, outputs=2, hidden_layer_size=5)
w = nn.initialize_random_weights()
outputs = nn.propagate(np.random.rand(12), w)

gui = GFX(weights=w)

print(gui.main(True))


def genetics(generation_size=1000, population_size=100, survivors_size=5):
    population = []
    for r in range(population_size):
        """ Since we are starting the population, we don't send weights so that they are created randomly"""
        population.append(GFX())

    for generation in range(generation_size):
        fitness = np.array([robot.main(False) for robot in population])
        survivors_ind = np.argpartition(fitness, -survivors_size)[-survivors_size:]
        survivors = population[survivors_ind]
        random.shuffle(survivors)
        parent_1, parent_2 = survivors[:2]
        for robot in population:



