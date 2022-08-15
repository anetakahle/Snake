# Dense layer
class Layer_Dense:
 # Layer initialization
    def __init__(self, n_inputs, n_neurons):
        # Initialize weights and biases
        self.weights = 0.10 * np.random.randn(n_inputs, n_neurons) #already transposed matrix of weights for every neuron
        self.biases = np.zeros((1, n_neurons))
    # Forward pass
    def forward(self, inputs):
    # Calculate output values from inputs, weights and biases
        self.output = np.dot(inputs, self.weights) + self.biases
