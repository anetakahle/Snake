import random
import math
import numpy as np
from matplotlib import pyplot as pl
from time import sleep
from .internal import gameState as gs
from . import enums, serverConfig

class Server:

    # properties ----------------------
    world = []
    gameState = enums.gameStates.NotStarted
    score = 0
    size = 8
    config = serverConfig.defaultConfig

    # ctor ----------------------

    def __init__(self, config = serverConfig.defaultConfig):
        self.config = config
        self.init()
        return;

    # public ----------------------

    def init(self):
        self._reset()
        if self.config.mode == enums.serverModes.Auto:
            while self.config.gamesToPlay > 0:
                self.config.gamesToPlay -= 1
                self.config.newGameCallback(self.config.gamesToPlay)
                self._playGameAuto()
                # todo save snapshot
        return;

    def step(self, direction):
        self._step(direction)

    def getGameState(self):
        return gs.GameState(self);

    # private ------------------------------

    def _reset(self):
        self.gameState = enums.gameStates.AwaitingClient
        self.world = np.zeros((self.size, self.size), dtype=int)
        middle = [math.floor((self.size + 1) / 2) - 1, math.ceil((self.size + 1) / 2) - 1]
        y = random.randint(*middle)
        x = random.randint(*middle)
        self.world[y][x] = 1  # head
        self.world[y + 1][x] = 2  # body
        self._generateApple()
        return;

    def _playGameAuto(self):
        ttl = self.config.limitMovesPerGame
        while self._isGameRunning():
            action = self.config.fpsCallback(ttl)
            ttl -= 1

            if ttl < 0:
                break

            if action == enums.directions.Skip:
                continue

            self.step(action)

    def _generateApple(self):
        y = random.randint(0, self.size - 1)
        x = random.randint(0, self.size - 1)
        while self.world[y, x] != 0:
            y = random.randint(0, self.size - 1)
            x = random.randint(0, self.size - 1)
        self.world[y, x] = -1

    def _isGameRunning(self):
        return self.gameState == enums.gameStates.AwaitingServer or self.gameState == enums.gameStates.AwaitingClient;

    def _setGameState(self, state):
        self.gameState = state;

    def _step(self, action):
        apple_collected = False
        tail_value = 0
        head = None
        neck = None
        body = None
        tail = None
        for y in range(self.size):
            for x in range(self.size):
                if self.world[y][x] == 1:
                    head = [y, x]
                    self.world[y][x] += 1
                elif self.world[y][x] == 2:
                    neck = [y, x]
                    self.world[y][x] += 1
                elif self.world[y][x] > 2:
                    body = [y, x]
                    self.world[y][x] += 1
                if self.world[y][x] > tail_value:
                    tail = [y, x]
                    tail_value = self.world[y][x]
        if_apple = self.world[tail[0]][tail[1]]
        self.world[tail[0]][tail[1]] = 0
        y = head[0] - neck[0]
        x = head[1] - neck[1]
        look_dir = [y, x]
        look_dirs = [[0, -1], [-1, 0], [0, 1], [1, 0]]
        look_dir_index = look_dirs.index(look_dir)
        head_movement = None

        if action == enums.directions.Left:  # left
            head_movement = look_dirs[look_dir_index - 1]
        elif action == enums.directions.Forward:  # straight
            head_movement = look_dirs[look_dir_index]
        elif action == enums.directions.Right:  # right
            if look_dir_index == 3:
                head_movement = look_dirs[0]
            else:
                head_movement = look_dirs[look_dir_index + 1]

        new_head_y = head[0] + head_movement[0]
        new_head_x = head[1] + head_movement[1]

        if (new_head_x > self.size - 1) or (new_head_y > self.size - 1) or (new_head_x < 0) or (new_head_y < 0) or (
                self.world[new_head_y][new_head_x] > 1):
            self._setGameState(enums.gameStates.Finished)

        if self._isGameRunning():
            if self.world[new_head_y][new_head_x] == -1:
                apple_collected = True
                self.world[tail[0]][tail[1]] = if_apple
            self.world[new_head_y][new_head_x] = 1

        self._postStep(apple_collected)

    def _postStep(self, apple_collected):
        if self.gameState == enums.gameStates.Finished:
            self.score = 0
            self.gameState = enums.gameStates.NotStarted
            self._reset()

        if apple_collected is True:
            self._generateApple()
            self.score += 1