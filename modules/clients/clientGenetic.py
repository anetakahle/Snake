import numpy as np
from modules import enums, server
from modules.clients.base import clientAiBase as caib
from modules.GeneticAI import Activation_ReLU as relu, Dense_Layer as denl
from modules.snakeViews import snakeViewRel3DirDist1 as sw1


class ClientGenetic(caib.ClientAiBase):

    # properties ------------

    actionsPerSecond = 0.1
    inputLayerSize = 6
    inputLayer = np.zeros(inputLayerSize)
    server : server = None
    sw1 = object
    lastValues = [[0, 0 ,0]]
    hiddenLayers = []

    # ctor -----------

    def setupLayers(self):
        self.hiddenLayers = []
        self.hiddenLayers.append(denl.Layer_Dense(len(self.inputLayer), self.inputLayerSize, enums.weightModes.Random, enums.biasModes.Random))
        self.hiddenLayers.append(denl.Layer_Dense(self.inputLayerSize, self.inputLayerSize))
        self.hiddenLayers.append(denl.Layer_Dense(self.inputLayerSize, 3))

    def init(self):
        self.sw1 = sw1.SnakeView1(self)

    # public ------------

    def onFrame(self):
        self.render.log("Vaha doleva: " + str(self.lastValues[0][0]), enums.logTypes.Ok)
        self.render.log("Vaha Rovne: " + str(self.lastValues[0][1]), enums.logTypes.Ok)
        self.render.log("Vaha doprava: " + str(self.lastValues[0][2]), enums.logTypes.Ok)

        for i in range(8):
            scanResult = self.server.scanDir8(enums.directions8(i), 2)
            self.render.log("Scan 8 (" + str(enums.directions8(i)) + "): " + str(scanResult), enums.logTypes.Ok)

    def computeLayers(self):
        self.inputLayer = self.createInputLayer()

        # LAYER 1
        dense1 = self.hiddenLayers[0]
        activation1 = relu.Activation_ReLU()
        dense1.forward(self.inputLayer)
        activation1.forward(dense1.output)

        # LAYER 2
        dense2 = self.hiddenLayers[1]
        activation2 = relu.Activation_ReLU()
        dense2.forward(activation1.output)
        activation2.forward(dense2.output)

        # OUTPUT LAYER
        layerOut = self.hiddenLayers[2]
        activationLayerOut = relu.Activation_ReLU()
        layerOut.forward(activation2.output)
        activationLayerOut.forward(layerOut.output)
        output = activationLayerOut.output

        return output

    def postBrain(self):
        output = self.computeLayers()
        self.lastValues = output

    def brain(self):

        # INPUT
        output = self.computeLayers()

        # ACTION SELECTION

        actionIndex = np.argmax(output[0])
        if actionIndex == 0:
            return enums.directions.Left
        elif actionIndex == 1:
            return enums.directions.Forward
        else:
            return enums.directions.Right



    # private ------------

    def createInputLayer(self, distance = 1): #translating a snake view into the input for the NN
        secondaryView = []
        secondaryViewApples = []
        secondaryViewObstacles = []
        for obj in self.sw1.getViewDist1(distance):
            if obj == enums.getInt(enums.gameObjects.Apple):
                secondaryViewApples.append(1)
            else:
                secondaryViewApples.append(0)

            if obj == enums.getInt(enums.gameObjects.Body) or obj == enums.getInt(enums.gameObjects.OutsideOfBounds):
                secondaryViewObstacles.append(1)
            else:
                secondaryViewObstacles.append(0)
        secondaryView += secondaryViewApples
        secondaryView += secondaryViewObstacles
        return secondaryView
