from src.gui import GFX
from src.neuralnet import *

# Test NN
nn = RNN(inputs=12, outputs=2, hidden_layer_size=5)
w = nn.initialize_random_weights()
outputs = nn.propagate(np.random.rand(12), w)

gui = GFX()
