import random

import modules.enums as enums
import modules.agents.base.clientAiBase as cb
import modules.serverReporter as serverReporter


class AgentRandom(cb.ClientAiBase):

    # properties ------------

    actionsPerSecond = 30

    # ctor -----------

    def init(self):
        pass

    # public ------------

    def onFrame(self):
        pass

    def mixLayers(self, prevGen : list[serverReporter.ServerReporter], clientIndex : int, clientsCount : int):
        pass

    def setupLayers(self):
        pass

    def brain(self):
        return random.choice([enums.directions.Forward, enums.directions.Right, enums.directions.Left])

    def getFitness(self) -> int:
        return 0

