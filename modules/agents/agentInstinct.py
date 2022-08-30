from modules import enums
from modules.agents.base import agentAiBase as caib
import modules.serverReporter as serverReporter
import modules.agents.base.agentAiBaseConfig as clientAiBaseConfig
import modules.instinctAi.instinct as instinct
import modules.instinctAi.network as network
import modules.server as serverNs
from modules.snakeViews import snakeViewR8DEndNearest as sw8n

class AgentInstinct(caib.AgentAiBase):

    # properties ------------------

    instinctInst : instinct.Instinct = None
    instinctNetwork : network.Network = None
    actionsPerSecond = 1
    server : serverNs.Server = None
    sw8n = object
    dbId = 1
    lastOutput : list[float] = []

    # ctor -----------------

    def __init__(self, instinctInst : instinct, instinctNetwork : network, config = clientAiBaseConfig.defaultClientAiBaseConfig):
        self.instinctInst = instinctInst
        self.instinctNetwork = instinctNetwork
        self.lastOutput = []
        super().__init__(config)

    # public ----------------

    def mixLayers(self, prevGen: list[serverReporter.ServerReporter], clientIndex: int, clientsCount: int):
        pass

    def setupLayers(self):
        pass

    def init(self):
        self.sw8n = sw8n.SnakeViewR8DEndNearest(self)
        pass

    def onFrame(self):
        if len(self.lastOutput) >= 3:
            self.render.log("Vaha doleva: " + str(self.lastOutput[0]), enums.logTypes.Ok)
            self.render.log("Vaha Rovne: " + str(self.lastOutput[1]), enums.logTypes.Ok)
            self.render.log("Vaha doprava: " + str(self.lastOutput[2]), enums.logTypes.Ok)

    def onAppleCollected(self):
        self.instinctNetwork.updateScore(5)

    def brain(self) -> enums.directions:

        input = self.createInput()
        output = self.instinctNetwork.activate(input)
        self.lastOutput = output

        actionIndex = output.index(max(output))
        self.instinctNetwork.updateScore(1)

        if actionIndex == 0:
            return enums.directions.Left
        elif actionIndex == 1:
            return enums.directions.Forward
        else:
            return enums.directions.Right

    def getFitness(self) -> int:
        return 0

    def createInput(self):  # translating a snake view into the input for the NN
        secondaryView = []
        secondaryViewApples = []
        secondaryViewObstacles = []
        for obj, dis in self.sw8n.getViewR8DEndNearest():
            if obj == enums.getInt(enums.gameObjects.Apple):
                secondaryViewApples.append(1)
            else:
                secondaryViewApples.append(0)

            if obj == enums.getInt(enums.gameObjects.Body) or obj == enums.getInt(
                    enums.gameObjects.OutsideOfBounds) or obj == enums.getInt(enums.gameObjects.Neck):
                secondaryViewObstacles.append(1)
            else:
                secondaryViewObstacles.append(0)
        secondaryView += secondaryViewApples
        secondaryView += secondaryViewObstacles
        # secondaryView.append(self.server.distanceBetweenManhattan(enums.gameObjects.Head, enums.gameObjects.Apple))
        return secondaryView


    # private ------------------------






