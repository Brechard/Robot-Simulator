"""
The goal of the experiment is to find optimal noise parameters inputted into Karman Filter
that will result in a
"""

from view.gui import GFX


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
    gui.main(draw=False, max_time=max_time, kill_when_stuck=False)

    # Get the values




