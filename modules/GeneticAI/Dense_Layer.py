import  modules.enums as enums
import numpy as np

# Dense layer
class Layer_Dense:
 # Layer initialization
    def __init__(self, n_inputs, n_neurons, weightsMode = enums.weightModes.Random, biasMode = enums.biasModes.Zero):
        # Initialize weights and biases
        if weightsMode == enums.weightModes.Random:
            self.weights = 0.10 * np.random.randn(n_inputs, n_neurons) #already transposed matrix of weights for every neuron
        elif weightsMode == enums.weightModes.Zero:
            self.weights = np.zeros(n_inputs, n_neurons)
        elif weightsMode == enums.weightModes.One:
            self.weights = np.ones((n_inputs, n_neurons))
        if biasMode == enums.biasModes.Random:
            self.biases = (0.10 * np.random.randn(1, n_neurons))[0]
        elif biasMode == enums.biasModes.Zero:
            self.biases = (np.zeros((1, n_neurons)))[0]
        elif biasMode == enums.biasModes.One:
            self.biases = (np.ones((1, n_neurons)))[0]
    # Forward pass
    def forward(self, inputs):
    # Calculate output values from inputs, weights and biases
        temp = np.dot(inputs, self.weights)
        self.output = temp + self.biases
