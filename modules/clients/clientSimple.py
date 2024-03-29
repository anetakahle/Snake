import random
import modules.enums as enums
import modules.clients.base.clientAiBase as cb
from modules import serverReporter as serverReporter


class ClientSimple(cb.ClientAiBase):

    # properties ------------

    actionsPerSecond = 20

    # ctor -----------

    def init(self):
        pass

    # public ------------


    def brain(self):
        if self.server.scanDirEq(enums.directions.Left, enums.gameObjects.Apple):
            return enums.directions.Left
        elif self.server.scanDirEq(enums.directions.Right, enums.gameObjects.Apple):
            return enums.directions.Right
        elif self.server.scanDirEq(enums.directions.Forward, enums.gameObjects.Apple):
            return enums.directions.Forward

        if self.server.scanDirBlocked(enums.directions.Forward):
            if self.server.scanDirBlocked(enums.directions.Right):
                return enums.directions.Left
            elif self.server.scanDirBlocked(enums.directions.Left):
                return enums.directions.Right
            return random.choice([enums.directions.Left, enums.directions.Right])

        possibleActions = [enums.directions.Forward]
        if not self.server.scanDirBlocked(enums.directions.Right):
            possibleActions.append(enums.directions.Right)
        if not self.server.scanDirBlocked(enums.directions.Left):
            possibleActions.append(enums.directions.Left)
        return random.choice(possibleActions)

    def mixLayers(self, prevGen: list[serverReporter.ServerReporter], clientIndex: int, clientsCount: int):
        pass

    def getFitness(self) -> int:
        return 0

    def setupLayers(self):
        pass

    def onFrame(self):
        pass



