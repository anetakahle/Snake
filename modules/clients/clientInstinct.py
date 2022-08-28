import random
import numpy as np
from modules import enums, server
from modules.clients.base import clientAiBase as caib
from modules.snakeViews import snakeViewR8DEndNearest as sw8n
import sqlite3
import modules.serverReporter as serverReporter
import modules.clients.base.clientAiBaseConfig as clientAiBaseConfig
import modules.instinctAi.instinct as instinct
import modules.instinctAi.network as graph

class ClientInstinct(caib.ClientAiBase):

    # properties ------------------

    instinctInst : instinct = None
    instinctGraph : graph = None

    # ctor -----------------

    def __init__(self, instinctInst : instinct, instinctGraph : graph, config = clientAiBaseConfig.defaultClientAiBaseConfig):
        self.instinctInst = instinct
        self.instinctGraph = graph
        super().__init__(config)

    def mixLayers(self, prevGen: list[serverReporter.ServerReporter], clientIndex: int, clientsCount: int):
        pass

    def setupLayers(self):
        pass

    def init(self):
        pass

    def onFrame(self):
        pass

    def brain(self) -> enums.directions:
        return enums.directions.Forward

    def getFitness(self) -> int:
        return 0

    # properties ------------

    actionsPerSecond = 1
    server : server = None
    sw8n = object
    dbId = 1

    # public ----------------


    # private ------------------------






