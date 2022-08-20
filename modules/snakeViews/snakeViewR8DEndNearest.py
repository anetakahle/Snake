import modules.clients.base.clientAiBase as cb
import modules.enums as enums

class SnakeView1():

    # properties ------------
    client = object

    # ctor -----------

    def __init__(self, client : cb.ClientAiBase):
        self.client = client

    # public ------------



    def getView(self):
        # vidime do konce, 8 smeru relativne k hlave
        # [L, FL, F, FR, R, BR, B, BL]
        ll = [None, None, None, None, None, None, None, None]

        distance = 1
        while any(ll, lambda x: x is None):
            for idx, ii in enumerate(ll):
                if ii is not None:

                    jj = self.client.server.scanDir(enums.directions8(idx), distance)
                    if jj != enums.gameObjects.Void:
                        ll[idx] = jj
            distance += 1







        L = self.client.server.scanDir(enums.directions.Left, distance)
        F = self.client.server.scanDir(enums.directions.Forward, distance)
        R = self.client.server.scanDir(enums.directions.Right, distance)
        return ll