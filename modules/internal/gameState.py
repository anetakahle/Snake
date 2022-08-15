import numpy as np
from modules import enums, server


class GameState:

    # properties ----------------

    world = np.zeros((1, 1), dtype=int)
    gameState = enums.gameStates.NotSet
    width = 0
    height = 0
    score = 0

    # ctor ---------------

    def __init__(self, server):
        self.world = server.world
        self.gameState = server.gameState
        self.score = server.score
        self.width = server.size
        self.height = server.size

    # public ---------------

    def iterateWorld(self, iterator = lambda x, y, val: None):
        for y in range(self.width):
            for x in range(self.width):
                iterator(x, y, self.world[y][x])
