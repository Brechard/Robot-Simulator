import numpy as np


class RNN:

    def __init__(self, inputs=12, outputs=2, hidden_layer_size=5, weights=None):
        """
        When weights is not passed they will be created as random
        :param inputs: Corresponds to the number of sensors
        :param outputs: Corresponds to the speed of the motors
        :param hidden_layer_size: Size of the hidden layer
        :param weights: Weights of the RNN
        """
        self.inputs = inputs
        self.recurrent_nodes = outputs
        self.outputs = outputs
        self.hidden_layer = hidden_layer_size
        self.last_outputs = np.zeros(outputs)
        if weights is not None:
            self.unflatten(weights)
        else:
            self.weights = self.initialize_random_weights()

    def initialize_random_weights(self, limit=.5):
        total_weights = (self.inputs + self.recurrent_nodes) * self.hidden_layer + self.hidden_layer * self.outputs
        # input_weights = np.random.uniform(-limit, limit, (self.inputs + self.recurrent_nodes, self.hidden_layer))
        # output_weights = np.random.uniform(-limit, limit, (self.hidden_layer, self.outputs))
        # self.weights = [input_weights, output_weights]
        # return self.flatten()
        return np.random.uniform(-limit, limit, total_weights)

    def flatten(self):
        weights = []
        for w in self.weights:
            weights.append(w.flatten().tolist())
        return [item for sublist in weights for item in sublist]

    def unflatten(self, weights):
        self.weights = []
        weights = np.asarray(weights)
        hidden_layer = weights[:(self.inputs + self.recurrent_nodes)*self.hidden_layer]
        self.weights.append(hidden_layer.reshape((self.inputs + self.recurrent_nodes, self.hidden_layer)))
        output_layer = weights[(self.inputs + self.recurrent_nodes)*self.hidden_layer:]
        self.weights.append(output_layer.reshape((self.hidden_layer, self.outputs)))

    def propagate(self, inputs, weights=None):
        # Add previous output as recurrent input
        values = np.append(inputs, self.last_outputs)

        # Set weights
        if weights is not None:
            self.unflatten(weights)

        # Propagate
        for weights in self.weights:
            values = np.tanh(np.matmul(values, weights))

        self.last_outputs = values
        return values