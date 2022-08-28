from modules import enums, server
from modules.clients.base import clientAiBase as caib
import modules.serverReporter as serverReporter
import modules.clients.base.clientAiBaseConfig as clientAiBaseConfig
import modules.instinctAi.instinct as instinct
import modules.instinctAi.network as network
from modules.snakeViews import snakeViewR8DEndNearest as sw8n

class ClientInstinct(caib.ClientAiBase):

    # properties ------------------

    instinctInst : instinct = None
    instinctNetwork : network = None
    sw8n = object

    # ctor -----------------

    def __init__(self, instinctInst : instinct, instinctNetwork : network, config = clientAiBaseConfig.defaultClientAiBaseConfig):
        self.instinctInst = instinctInst
        self.instinctNetwork = instinctNetwork
        super().__init__(config)

    def mixLayers(self, prevGen: list[serverReporter.ServerReporter], clientIndex: int, clientsCount: int):
        pass

    def setupLayers(self):
        pass

    def init(self):
        self.sw8n = sw8n.SnakeViewR8DEndNearest(self)
        pass

    def onFrame(self):
        pass

    def brain(self) -> enums.directions:

        input = self.createInput()
        output = self.instinctNetwork.activate(input)

        actionIndex = output.index(max(output))

        if actionIndex == 0:
            return enums.directions.Left
        elif actionIndex == 1:
            return enums.directions.Forward
        else:
            return enums.directions.Right

    def getFitness(self) -> int:
        return 0

    # properties ------------

    actionsPerSecond = 1
    server : server = None
    sw8n = object
    dbId = 1

    # public ----------------

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






