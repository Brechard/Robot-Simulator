class Experiments:
    def __init__(self):
        self.position_observed_error = []
        self.position_predicted_error = []
        self.position_kalman_error = []

    def calculate_errors(self, real_pos, obs_pos, pred_pos, kalman_pos):
        mse = ((real_pos - obs_pos) ** 2).mean(axis=0)
        self.position_observed_error.append(mse)

        mse = ((real_pos - pred_pos) ** 2).mean(axis=0)
        self.position_observed_error.append(mse)

        mse = ((real_pos - kalman_pos) ** 2).mean(axis=0)
        self.position_observed_error.append(mse)
