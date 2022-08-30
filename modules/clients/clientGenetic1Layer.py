import random
import numpy as np
from modules import enums, server
from modules.clients.base import clientAiBase as caib
from modules.GeneticAI import Activation_ReLU as relu, Activation_Sigmoid as sigmoid, Dense_Layer as denl
from modules.snakeViews import snakeViewR8DEndNearest as sw8n
from modules import masterServer as masterServer
import sqlite3
import modules.serverReporter as serverReporter

class ClientGenetic2(caib.ClientAiBase):

    # properties ------------

    actionsPerSecond = 1
    inputLayerSize = 8 #num of neurons
    inputLayer = np.zeros(inputLayerSize)
    server : server = None
    sw8n = object
    lastValues : list[float] = []
    hiddenLayers = []
    dbId = 1
    input = []

    # public ------------

    def getFitness(self) -> int :
        score = self.server.score * 5
        score += self.server.movesCount

        if self.server.gameEndReason == enums.gameEndReasons.MovesLimitExceeded or self.server.gameEndReason == enums.gameEndReasons.AppleNotCollectedInLimit or self.server.gameEndReason == enums.gameEndReasons.TurnStrikeLimitExceeded:
            score = 0

        return score

    def mixLayers(self, prevGen : list[serverReporter.ServerReporter], clientIndex : int, clientsCount : int):
        useTopMax = 1
        indexToUse = clientIndex // (clientsCount // useTopMax)
        ancestor = prevGen[indexToUse]
        ancestorB = prevGen[indexToUse + 1]

        self.hiddenLayers = ancestor.server.client.hiddenLayers

        doCrossover = False
        doMutation = False
        mutationFactor = 0.01

        # crossover
        if doCrossover:
            hlIndex = 0
            for hl in self.hiddenLayers:
                pivotW = random.randrange(0, len(hl.weights))
                pivotB = random.randrange(0, len(hl.biases))

                for i in range(pivotW, len(hl.weights) - 1):
                    for innerIndex, innerVal in np.ndenumerate(hl.weights[i]):
                        hl.weights[i][innerIndex] = ancestorB.server.client.hiddenLayers[hlIndex].weights[i][innerIndex]
                for i in range(pivotB, len(hl.biases) - 1):
                    hl.biases[i] = ancestorB.server.client.hiddenLayers[hlIndex].biases[i]

                hlIndex += 1

        # mutation
        if doMutation:
            for hl in self.hiddenLayers:
                for index in range(len(hl.weights)):
                    for innerIndex, innerVal in np.ndenumerate(hl.weights[index]):
                        hl.weights[index][innerIndex] += random.uniform(-mutationFactor, mutationFactor)
                for index, val in enumerate(hl.biases):
                    hl.biases[index] += random.uniform(-mutationFactor, mutationFactor)

    def setupLayers(self):
        self.hiddenLayers = []
        self.input = self.createInput()
        self.hiddenLayers.append(denl.Layer_Dense(len(self.input), self.inputLayerSize, enums.weightModes.Random, enums.biasModes.Random))
        self.hiddenLayers.append(denl.Layer_Dense(self.inputLayerSize, 3))

    def init(self):
        self.sw8n = sw8n.SnakeViewR8DEndNearest(self)
        self.config.dbId = 1

    def onFrame(self):

        if len(self.lastValues) >= 3:
            self.render.log("Vaha doleva: " + str(self.lastValues[0]), enums.logTypes.Ok)
            self.render.log("Vaha Rovne: " + str(self.lastValues[1]), enums.logTypes.Ok)
            self.render.log("Vaha doprava: " + str(self.lastValues[2]), enums.logTypes.Ok)

        viewResult = self.sw8n.getViewR8DEndNearest()
        for entry in viewResult:
            self.render.log("View 8 (" + str(entry) + "): " + str(viewResult), enums.logTypes.Ok)


    def computeLayers(self):
        self.input = self.createInput()

        sigmoidLayer = sigmoid.Activation_Sigmoid()

        # INPUT LAYER
        dense1 = self.hiddenLayers[0]
        dense1.forward(self.input)
        sigmoidLayer.forward(dense1.output)

        # OUTPUT LAYER
        layerOut = self.hiddenLayers[1]
        layerOut.forward(sigmoidLayer.output)
        sigmoidLayer.forward(layerOut.output)

        output = sigmoidLayer.output
        return output

    def postBrain(self):
        output = self.computeLayers()
        self.lastValues = output


    def brain(self):

        # INPUT
        output = self.computeLayers()

        # ACTION SELECTION
        maxValIdx = np.argmax(output)
        #ActionsToSelect = []
        #epsilon = 0.001

        # pro ty idx, ktere se nerovnaji maxvalidx, vyber ty, co se lisi nanejvys o E
        #for i in range(3):
        #    if output[maxValIdx] - output[i] <= epsilon:
        #        ActionsToSelect.append(i)

        #actionIndex = random.choice(ActionsToSelect)
        actionIndex = maxValIdx

        if actionIndex == 0:
            return enums.directions.Left
        elif actionIndex == 1:
            return enums.directions.Forward
        else:
            return enums.directions.Right



    # private ------------

    def createInput(self): #translating a snake view into the input for the NN
        secondaryView = []
        secondaryViewApples = []
        secondaryViewObstacles = []
        for obj, dis in self.sw8n.getViewR8DEndNearest():
            if obj == enums.getInt(enums.gameObjects.Apple):
                secondaryViewApples.append(1)
            else:
                secondaryViewApples.append(0)

            if obj == enums.getInt(enums.gameObjects.Body) or obj == enums.getInt(enums.gameObjects.OutsideOfBounds) or obj == enums.getInt(enums.gameObjects.Neck):
                secondaryViewObstacles.append(1)
            else:
                secondaryViewObstacles.append(0)
        secondaryView += secondaryViewApples
        secondaryView += secondaryViewObstacles
        #secondaryView.append(self.server.distanceBetweenManhattan(enums.gameObjects.Head, enums.gameObjects.Apple))
        return secondaryView
