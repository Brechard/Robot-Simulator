import genetic_algorithm
from gui import GFX
from robot import Robot

# best_robot = genetic_algorithm.genetics(load_population=True, n_generation=1)

gui = GFX()
gui.set_robot(Robot(genetic_algorithm.WIDTH, genetic_algorithm.HEIGHT, genetic_algorithm.wall_list))
gui.main(True, 10000)
