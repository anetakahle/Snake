from __future__ import annotations
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


    # ctor -------------------

    def __init__(self, inputSize : int, outputSize : int, populationSize : int, topPercentToUse : float, mutationRate : float, mutationAmount : float, fitnessFn : enums.activationFunctions = enums.activationFunctions.Logistic):
        self.inputSize = inputSize
        self.outputSize = outputSize
        self.populationSize = populationSize
        self.topPercentToUse = topPercentToUse
        self.mutationAmount = mutationAmount
        self.mutationRate = mutationRate
        self.fitnessFn = fitnessFn
        self.population = []

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


