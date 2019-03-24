import numpy as np


def kalman_filter(state, covariance, control, observation):
    """
    :param state: Previous believe state
    :param covariance: Covariance matrix
    :param control: kinematics values
    :param observation:
    :return:
    """

    # Initialing distributions
    A = np.identity(3)
    B = np.array([[np.cos(state[2]), 0],
                  [np.sin(state[2]), 0],
                  [0, 1]])
    C = np.identity(3)
    R = np.identity(3) * np.random.rand(3, 1) * 0.1  # Covariance matrix defining noise of motion model epsilon
    Q_t = np.identity(3) * np.random.rand(3, 1) * 0.1  # Covariance matrix defining noise of motion model delta

    # Prediction
    state = np.matmul(A, state) + np.matmul(B, control)  # mu_t
    covariance = np.matmul(np.matmul(A, covariance), A.T) + R  # sum_t

    # Correction
    K_t = covariance * C.T * np.linalg.inv(np.matmul(np.matmul(C, covariance), C.T) + Q_t.T)  # Kalman gain
    try:
        new_state = state + np.matmul(K_t, (observation - np.matmul(C, state)))
    except:
        print("ERROR")
    new_covariance = np.matmul((np.identity(3) - np.matmul(K_t, C)), covariance)

    return state, new_state, new_covariance
