import random
import numpy as np
from modules import enums, server
from modules.agents.base import agentAiBase as caib
from modules.GeneticAI import Activation_ReLU as relu, Dense_Layer as denl
from modules.snakeViews import snakeViewR8DEndNearest as sw8n
import sqlite3
import modules.serverReporter as serverReporter


class AgentGenetic(caib.AgentAiBase):

    # properties ------------

    actionsPerSecond = 1
    inputLayerSize = 16
    inputLayer = np.zeros(inputLayerSize)
    server : server = None
    sw8n = object
    lastValues = [[0, 0 ,0]]
    hiddenLayers = []
    dbId = 1

    # public ------------

    def getFitness(self) -> int :
        score = self.server.score * 5
        score += self.server.movesCount

        if self.server.gameEndReason == enums.gameEndReasons.MovesLimitExceeded or self.server.gameEndReason == enums.gameEndReasons.AppleNotCollectedInLimit or self.server.gameEndReason == enums.gameEndReasons.TurnStrikeLimitExceeded:
            score = 0

        return score

    def mixLayers(self, prevGen : list[serverReporter.ServerReporter], clientIndex : int, clientsCount : int):

        useTopMax = 2
        indexToUse = clientIndex // (clientsCount // useTopMax)
        ancestor = prevGen[indexToUse]

        self.hiddenLayers = ancestor.server.client.hiddenLayers

        for hl in self.hiddenLayers:
            for index, val in enumerate(hl.weights):
                hl.weights[index] += random.uniform(-0.1, 0.1)
            for index, val in enumerate(hl.biases):
                hl.biases[index] += random.uniform(-0.1, 0.1)

    def setupLayers(self):
        self.hiddenLayers = []
        self.hiddenLayers.append(denl.Layer_Dense(len(self.inputLayer), self.inputLayerSize, enums.weightModes.Random, enums.biasModes.Random))
        self.hiddenLayers.append(denl.Layer_Dense(self.inputLayerSize, self.inputLayerSize))
        self.hiddenLayers.append(denl.Layer_Dense(self.inputLayerSize, 3))

    def init(self):
        self.sw8n = sw8n.SnakeViewR8DEndNearest(self)
        self.config.dbId = 1

    def onFrame(self):
        if len(self.lastValues) >= 3:
            self.render.log("Vaha doleva: " + str(self.lastValues[0]), enums.logTypes.Ok)
            self.render.log("Vaha Rovne: " + str(self.lastValues[1]), enums.logTypes.Ok)
            self.render.log("Vaha doprava: " + str(self.lastValues[2]), enums.logTypes.Ok)

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
        maxValIdx = np.argmax(output)
        ActionsToSelect = []
        epsilon = 0.001

        # pro ty idx, ktere se nerovnaji maxvalidx, vyber ty, co se lisi nanejvys o E
        for i in range(3):
            if output[maxValIdx] - output[i] <= epsilon:
                ActionsToSelect.append(i)

        actionIndex = random.choice(ActionsToSelect)


        if actionIndex == 0:
            return enums.directions.Left
        elif actionIndex == 1:
            return enums.directions.Forward
        else:
            return enums.directions.Right



    # private ------------

    def createInputLayer(self): #translating a snake view into the input for the NN
        secondaryView = []
        secondaryViewApples = []
        secondaryViewObstacles = []
        for obj, dis in self.sw8n.getViewR8DEndNearest():
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
