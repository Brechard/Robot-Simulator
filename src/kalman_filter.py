import numpy as np


def kalman_filter(state, covariance, control, observation):
    """
    :param state:
    :param covariance:
    :param control:
    :param observation:
    :return:
    """

    # Initialing distributions
    A = np.identity(3)
    B = np.array([[np.cos(state[2]), 0],
                  [np.sin(state[2]), 0],
                  [0, 1]])
    C = np.identity(3)
    R = np.identity(3) * np.random.rand(3, 1) * 0.1

    # Prediction
    state = np.matmul(A, state) + np.matmul(B, control)
    covariance = np.matmul(np.matmul(A, covariance), A.T) + R

    # Correction

    return state, covariance
