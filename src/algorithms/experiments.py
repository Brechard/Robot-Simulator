import numpy as np


class Experiments:
    def __init__(self):
        self.position_observed_error = [[], [], []]
        self.position_predicted_error = [[], [], []]
        self.position_kalman_error = [[], [], []]

        keys = ['observed', 'predicted', 'kalman']
        self.errors = dict.fromkeys(keys)
        for key, values in self.errors.items():
            self.errors[key] = []

    def calculate_errors(self, real_pos, obs_pos, pred_pos, kalman_pos):
        self.errors['observed'] = self.calculate_mean_squared_errors_normalized(obs_pos, real_pos)
        self.errors['predicted'] = self.calculate_mean_squared_errors_normalized(obs_pos, pred_pos)
        self.errors['kalman'] = self.calculate_mean_squared_errors_normalized(obs_pos, kalman_pos)

    def calculate_mean_squared_errors_normalized(self, calculated_position, real_position):
        result = []
        for idx in range(len(real_position)):
            error = real_position[idx] - calculated_position[idx]
            variance = np.var(error)
            error = error ** 2 / variance
            result.append(error)
        return result
