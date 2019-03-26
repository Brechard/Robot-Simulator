class Experiments:
    def __init__(self):
        self.position_observed_error = [[], [], []]
        self.position_predicted_error = [[], [], []]
        self.position_kalman_error = [[], [], []]

    def calculate_errors(self, real_pos, obs_pos, pred_pos, kalman_pos):
        error_x = (real_pos[0] - obs_pos[0])
        error_y = (real_pos[1] - obs_pos[1])
        error_a = (real_pos[2] - obs_pos[2])
        self.position_observed_error[0].append(error_x)
        self.position_observed_error[1].append(error_y)
        self.position_observed_error[2].append(error_a)

        error_x = (real_pos[0] - pred_pos[0])
        error_y = (real_pos[1] - pred_pos[1])
        error_a = (real_pos[2] - pred_pos[2])
        self.position_predicted_error[0].append(error_x)
        self.position_predicted_error[1].append(error_y)
        self.position_predicted_error[2].append(error_a)

        error_x = (real_pos[0] - kalman_pos[0])
        error_y = (real_pos[1] - kalman_pos[1])
        error_a = (real_pos[2] - kalman_pos[2])
        self.position_kalman_error[0].append(error_x)
        self.position_kalman_error[1].append(error_y)
        self.position_kalman_error[2].append(error_a)
        
    def normalize(self):
        import numpy as np
        for i in range(len(self.position_observed_error)):
            var = np.var(self.position_observed_error[i])
            self.position_observed_error[i] = self.position_observed_error[i] ** 2 / var

