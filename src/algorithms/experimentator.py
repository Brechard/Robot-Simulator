"""
The goal of the experiment is to find optimal noise parameters inputted into Karman Filter
that will result in a
"""

from view.gui import GFX
import matplotlib.pyplot as plt
import csv
import numpy as np

default_Q_t = np.identity(3) * np.random.rand(3, 1) * 0.1
default_R = np.identity(3) * np.random.rand(3, 1) * 0.1

def run_observation_noise_experiment(Q, max_time, real_observation_noise):
    """
    :param Q: inputted noise of the sensor model
    :param num_of_iterations:
    :return:
    """
    # Initialize GUI
    gui = GFX()
    gui.robot.kalman_filter.Q_t = Q
    gui.robot.beacon_sensor_noise = real_observation_noise

    # Run simulation
    gui.main(draw=False, max_time=max_time, kill_when_stuck=False, use_steps=False)
    gui.experiments.calculate_errors()
    errors = gui.experiments.calculate_average()
    print(errors)
    return errors



    # # Get the values
    # plt.hist(gui.experiments.errors['observed'])
    # plt.title("Observed position error")
    # plt.show()
    #
    # plt.plot(gui.experiments.errors['predicted'])
    # plt.hist("Predicted position error")
    # plt.show()
    #
    # plt.hist(gui.experiments.errors['kalman'])
    # plt.title("Kalman position error")
    # plt.show()



Qs = np.linspace(0,.4,11)
Q_t = [np.identity(3) * (q ** 2) for q in Qs]
errors = []


for Q in Q_t:
    errors.append(run_observation_noise_experiment(Q, 1000, 0.1))



# Store in txt
temp = np.asarray(errors)
np.savetxt("experiment.csv", temp)
