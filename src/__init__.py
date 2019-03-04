import genetic_algorithm
from gui import GFX
from robot import Robot
import main

# best_robot = genetic_algorithm.genetics(load_population=True, n_generation=1)

# best_robot = genetic_algorithm.genetics(n_generation=50, population_size=20, n_selected=15, elitism=0.05, load_population=False, draw=True)
best_robot = genetic_algorithm.get_best_individual()

gui = GFX()
best_robot.set_pos(100,150,0)
# best_robot.set_pos(genetic_algorithm.WIDTH-100,150, 30)
# best_robot.set_pos(100, genetic_algorithm.HEIGHT - 150, 145)
gui.set_robot(best_robot)
gui.main(True, 10000)
