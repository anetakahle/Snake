import modules.agents.base.clientAiBase as cb
import modules.enums as enums

class SnakeViewR8DEndNearest():

    # properties ------------
    client = object

    # ctor -----------

    def __init__(self, client : cb.ClientAiBase):
        self.client = client

    # public ------------



    def getViewR8DEndNearest(self):
        # vidime do konce, 8 smeru relativne k hlave
        # [L, FL, F, FR, R, BR, B, BL]
        ll = [None, None, None, None, None, None, None, None]

        distance = 1
        while any(x is None for x in ll):
            for idx, ii in enumerate(ll):
                if ii is None:
                    jj = self.client.server.scanDir8(enums.directions8(idx), distance)
                    if jj != enums.gameObjects.Void:
                        ll[idx] = (jj, distance)
            distance += 1

        return ll