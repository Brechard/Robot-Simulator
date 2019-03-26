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
    gui.robot.kinematical_parameters = [1, 0]
    gui.robot.beacon_sensor_noise = 0.1
    gui.robot.kinematics_error = 0.1
    gui.robot.kalman_filter.R = np.identity(3) * 0.1

    # Run simulation
    gui.main(draw=True, max_time=max_time, kill_when_stuck=False, use_steps=False)

    gui.experiments.calculate_errors()
    errors = gui.experiments.calculate_average()
    print(errors)
    return errors


Qs = np.linspace(0.1, 10, 10)
Q_t = [np.identity(3) * (q ** 2) for q in Qs]
errors = []

for i, Q in enumerate(Q_t):
    error = run_observation_noise_experiment(Q, 1000, Qs[i])
    errors.append(error)


# Store in txt
temp = np.asarray(errors).T
plt.plot(Qs, temp[0], label="Error in X")
plt.plot(Qs, temp[1], label="Error in Y")
plt.xlabel("Variance")
plt.ylabel("Error")
plt.legend()
plt.show()

plt.plot(Qs, temp[2], label="Error in theta")
plt.xlabel("Variance")
plt.ylabel("Error")
plt.legend()
plt.show()

# np.savetxt("experiment.csv", temp)
