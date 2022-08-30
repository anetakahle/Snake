from __future__ import annotations

import math
import random
from typing import TYPE_CHECKING
import modules.instinctAi.network as network
import modules.enums as enums


class Instinct:

    # properties -----------------

    inputSize : int = 0
    outputSize : int = 0
    populationSize : int = 0
    topPercentToUse : float = 0.0
    mutationRate : float = 0.0
    mutationAmount : float = 0.0
    population : list[network.Network] = []
    fitnessFn : enums.activationFunctions = enums.activationFunctions.Logistic
    elitism : int = 0.2 * populationSize
    selection : enums.selectionMethods = enums.selectionMethods.Power


    # ctor -------------------

    def __init__(self, inputSize : int, outputSize : int, populationSize : int, topPercentToUse : float, mutationRate : float, mutationAmount : float, fitnessFn : enums.activationFunctions = enums.activationFunctions.Logistic, elitism : int = 0):
        self.inputSize = inputSize
        self.outputSize = outputSize
        self.populationSize = populationSize
        self.topPercentToUse = topPercentToUse
        self.mutationAmount = mutationAmount
        self.mutationRate = mutationRate
        self.fitnessFn = fitnessFn
        self.population = []
        self.elitism = elitism
        self.selection = enums.selectionMethods.Power
        # self.equal = equal

        self.createPool()

    # public -------------------

    def createPool(self):
        self.population = []

        for i in range(self.populationSize):
            nw = network.Network(self.inputSize, self.outputSize, 0)
            self.population.append(nw)


    def sortPopulationByScore(self) -> list[network.Network]:
        popSorted = sorted(self.population, key=lambda x: x.score, reverse=True)
        self.population = popSorted
        return popSorted

    def evaluate(self):
        pass

    def getOffspring(self):
        parent1 = self.getParent()
        parent2 = self.getParent()

        return network.Network.crossOver(parent1, parent2)

    def getParent(self):
        if self.selection == enums.selectionMethods.Power:
            if self.population[0].score < self.population[1].score:
                self.sortPopulationByScore()
            index = math.floor(math.pow(random.random(), enums.getInt(self.selection.PowerParamPower)) * len(self.population))
            return self.population[index]

        # todo implement rest of cases
        return self.population[0]