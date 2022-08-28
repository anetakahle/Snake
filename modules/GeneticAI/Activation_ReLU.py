
import modules.enums as enums
import numpy as np

# ReLU activation
class Activation_ReLU:
     # Forward pass
     def forward(self, inputs):
         # Calculate output values from input
         self.output = np.maximum(0, inputs)



