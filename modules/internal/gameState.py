import numpy as np
from .. import enums

class GameState:
    # properties ----------------

    world = np.zeros((1, 1), dtype=int)
    gameState = enums.gameStates.NotSet
    width = 8
    height = 8
    score = 0

    # ctor ---------------

    def __init__(self, world, gameState, score):
        self.world = world
        self.gameState = gameState
        self.score = score

