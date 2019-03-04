import genetic_algorithm
from gui import GFX
from robot import Robot
import main

# best_robot = genetic_algorithm.genetics(load_population=True, n_generation=1)
best_robot = genetic_algorithm.genetics()


# best_robot = genetic_algorithm.get_best_individual()

gui = GFX()
gui.set_robot(best_robot)
# gui.set_robot(Robot(genetic_algorithm.WIDTH, genetic_algorithm.HEIGHT, genetic_algorithm.wall_list))
gui.main(True, 10000)
