import random
import numpy as np
from modules import enums, server
from modules.clients.base import clientAiBase as caib
from modules.GeneticAI import Activation_ReLU as relu, Dense_Layer as denl
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
    lastValues = [[0, 0 ,0]]
    hiddenLayers = []
    dbId = 1
    input = []

    # public ------------

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
        self.input = self.createInput()

        self.hiddenLayers.append(denl.Layer_Dense(len(self.input), self.inputLayerSize, enums.weightModes.Random, enums.biasModes.Random))
        self.hiddenLayers.append(denl.Layer_Dense(self.inputLayerSize, 3))
        x = len(self.inputLayer)
        y = 0


    def init(self):
        self.sw8n = sw8n.SnakeViewR8DEndNearest(self)
        self.config.dbId = 1

    def onFrame(self):

        self.render.log("Vaha doleva: " + str(self.lastValues[0][0]), enums.logTypes.Ok)
        self.render.log("Vaha Rovne: " + str(self.lastValues[0][1]), enums.logTypes.Ok)
        self.render.log("Vaha doprava: " + str(self.lastValues[0][2]), enums.logTypes.Ok)

        for i in range(8):
            scanResult = self.server.scanDir8(enums.directions8(i), 2)
            self.render.log("Scan 8 (" + str(enums.directions8(i)) + "): " + str(scanResult), enums.logTypes.Ok)

    def computeLayers(self):



        # INPUT LAYER
        dense1 = self.hiddenLayers[0]
        # activation1 = relu.Activation_ReLU()
        dense1.forward(self.input)
        # activation1.forward(dense1.output)

        # OUTPUT LAYER
        layerOut = self.hiddenLayers[1]
        #activationLayerOut = relu.Activation_ReLU()
        layerOut.forward(dense1.output)
        #activationLayerOut.forward(layerOut.output)
        #output = activationLayerOut.output
        output = layerOut.output

        return output

    def postBrain(self):
        output = self.computeLayers()
        self.lastValues = output


    def brain(self):

        # INPUT
        output = self.computeLayers()

        # ACTION SELECTION
        output = output[0]
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
                secondaryViewApples.append(1/dis)
            else:
                secondaryViewApples.append(0)

            if obj == enums.getInt(enums.gameObjects.Body) or obj == enums.getInt(enums.gameObjects.OutsideOfBounds):
                secondaryViewObstacles.append(1/dis)
            else:
                secondaryViewObstacles.append(0)
        secondaryView += secondaryViewApples
        secondaryView += secondaryViewObstacles
        return secondaryView
