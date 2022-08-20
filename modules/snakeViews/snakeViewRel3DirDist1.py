import modules.clients.base.clientAiBase as cb
import modules.enums as enums

class SnakeView1():

    # properties ------------
    client = object

    # ctor -----------

    def __init__(self, client : cb.ClientAiBase):
        self.client = client

    # public ------------
    def getViewDist1(self, distance = 1):
        L = self.client.server.scanDir(enums.directions.Left, distance)
        F = self.client.server.scanDir(enums.directions.Forward, distance)
        R = self.client.server.scanDir(enums.directions.Right, distance)
        return [L, F, R]