import random

import modules.enums as enums
import modules.clients.base.clientAiBase as cb


class ClientRandom(cb.ClientAiBase):

    # properties ------------

    actionsPerSecond = 30

    # ctor -----------

    def init(self):
        pass

    # public ------------

    def brain(self):
        return random.choice([enums.directions.Forward, enums.directions.Right, enums.directions.Left])