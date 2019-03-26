import numpy as np


class Experiments:
    def __init__(self):
        self.position_real = []
        self.position_observed = []
        self.position_predicted = []
        self.position_kalman = []

        keys = ['observed', 'predicted', 'kalman']
        self.errors = dict.fromkeys(keys)
        for key, values in self.errors.items():
            self.errors[key] = []

    def store_values(self, real_pos, obs_pos, pred_pos, kalman_pos):
        self.position_real.append(real_pos)
        self.position_observed.append(obs_pos)
        self.position_predicted.append(pred_pos)
        self.position_kalman.append(kalman_pos)

    def calculate_errors(self):
        obs_pos = self.position_observed
        real_pos = self.position_real
        pred_pos = self.position_predicted
        kalman_pos = self.position_kalman
        self.errors['observed'] = np.array(self.calculate_mean_squared_errors_normalized(real_pos, obs_pos))
        self.errors['predicted'] = np.array(self.calculate_mean_squared_errors_normalized(real_pos, pred_pos))
        self.errors['kalman'] = np.array(self.calculate_mean_squared_errors_normalized(real_pos, kalman_pos))

        self.errors['observed']

    def calculate_mean_squared_errors_normalized(self, calculated_position, real_position):
        result = []
        for idx in range(len(real_position)):
            error = real_position[idx] - calculated_position[idx]
            result.append(error)
        variance = np.var(result)
        return [r ** 2 / variance for r in result]

    def calculate_average(self):
        self.position_real = np.array(self.position_real)
        self.position_kalman = np.array(self.position_kalman)
        self.average_errors = [(np.average((self.position_real[:, i] - self.position_kalman[:, i]) ** 2)) for i in
                               range(3)]
        return self.average_errors
