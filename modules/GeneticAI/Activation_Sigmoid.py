import modules.enums as enums
import numpy as np
import math

# Sigmoid activation
class Activation_Sigmoid:

     # Properties

     output : list[float] = []

     # Forward pass
     def forward(self, inputs):
         ll = []
         # Calculate output values from input
         for input in inputs:
            ll.append(1 / (1 + math.e ** (-input)))
         self.output = ll