"""
The goal of the experiment is to find optimal noise parameters inputted into Karman Filter
that will result in a
"""

from view.gui import GFX
import matplotlib.pyplot as plt


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
    gui.main(draw=True, max_time=max_time, kill_when_stuck=False)

    # Get the values
    plt.plot(gui.experiments.position_observed_error)

import numpy as np
default_Q_t = np.identity(3) * np.random.rand(3, 1) * 0.1
default_R = np.identity(3) * np.random.rand(3, 1) * 0.1

run_observation_noise_experiment(default_Q_t, 1000, default_Q_t)
