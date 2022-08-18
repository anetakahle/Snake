import random
import math
import numpy as np
from modules.internal import gameState as gs
from modules import enums, serverConfig
import modules.masterServer as ms

class Server:

    # properties ----------------------
    world = []
    gameState = enums.gameStates.NotStarted
    score = 0
    size = 8
    config = serverConfig.defaultConfig
    masterServer : ms.MasterServer = None
    clockFn = None

    # ctor ----------------------

    def __init__(self, config = serverConfig.defaultConfig):
        self.config = config
        self.init()
        return;

    # public ----------------------

    def init(self):
        self._newGame()
        if self.config.mode == enums.serverModes.Auto:
            while self.config.gamesToPlay > 0:
                self.config.gamesToPlay -= 1
                self.config.newGameCallback(self.config.gamesToPlay)
                self._playGameAuto()
        return;

    def getObject(self, object = enums.gameObjects.Head):
        xx = 0
        yy = 0
        for y in self.world:
            for x in y:
                if x == object.value:
                    return [xx, yy]
                xx += 1
            yy +=1
            xx = 0
        return [0, 0]

    def scanDirBlocked(self, direction = enums.directions.Forward, distance = 1):
        return self.scanDirEq(direction, enums.gameObjects.OutsideOfBounds) or self.scanDirEq(direction, enums.gameObjects.Body)

    def scanDirEq(self, direction = enums.directions.Forward, object = enums.gameObjects.Apple, distance = 1):
        x = enums.getInt(self.scanDir(direction, distance))

        if x > enums.getInt(enums.gameObjects.Neck):
            x = enums.getInt(enums.gameObjects.Body)

        return x == enums.getInt(object)

    def scanDir(self, direction = enums.directions.Forward, distance = 1):
        head = self.getObject(enums.gameObjects.Head)
        neck = self.getObject(enums.gameObjects.Neck)
        x = head[0] - neck[0]
        y = head[1] - neck[1]
        lookDir = [y, x]
        lookupTable = [[0, -1], [-1, 0], [0, 1], [1, 0]]
        lookupTableIndex = lookupTable.index(lookDir)

        if lookupTableIndex == 3 and direction == enums.directions.Right:
            shift = lookupTable[0]
        else:
            shift = lookupTable[lookupTableIndex + direction.value[0]]

        cellY = head[1] + distance * shift[0]
        cellX = head[0] + distance * shift[1]

        if (cellX > self.size - 1) or (cellY > self.size - 1) or (cellX < 0) or (cellY < 0):
            return enums.gameObjects.OutsideOfBounds

        return self.world[cellY, cellX]

    def scanRel(self, x, y):
        head = self.getObject(enums.gameObjects.Head)
        return self.world[head[1] + y, head[0] + x]

    def step(self, direction):

        if self.masterServer != None:
            self.masterServer.reportGameEvent(self, enums.gameCommands.ClientMove, {"direction": direction})

        self._step(direction)

    def getGameState(self):
        return gs.GameState(self);

    def setMasterServer(self, masterServer : ms.MasterServer):
        self.masterServer = masterServer
        masterServer.slaveServers.append(self)

    def setTickFn(self, function):
        self.clockFn = function

    def dispatchClockFn(self) -> bool:
        if self.clockFn == None:
            return False

        if self.config.gamesToPlay < 0:
            return False

        self.clockFn()

    # private ------------------------------

    def _newGame(self):

        if self.masterServer != None:
            self.masterServer.reportNewGame(self)

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

            if self.gameState == enums.gameStates.Finished:
                if self.masterServer != None:
                    self.masterServer.reportEndGame(self)

                self.score = 0
                self.gameState = enums.gameStates.NotStarted
                self._newGame()

    def _generateApple(self) -> (x, y):
        y = random.randint(0, self.size - 1)
        x = random.randint(0, self.size - 1)
        while self.world[y, x] != 0:
            y = random.randint(0, self.size - 1)
            x = random.randint(0, self.size - 1)
        self.world[y, x] = enums.getInt(enums.gameObjects.Apple)

        if self.masterServer != None:
            self.masterServer.reportGameEvent(self, enums.gameCommands.DestroyObject, {"object": "apple"})
            self.masterServer.reportGameEvent(self, enums.gameCommands.SpawnObject, {"object": "apple", "x": x, "y": y})

        return (x, y)

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
        lastTailPiece = self.world[tail[0]][tail[1]]
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
                self._incTail(tail[1], tail[0], lastTailPiece)
            self.world[new_head_y][new_head_x] = 1

        if apple_collected is True:
            self._generateApple()
            self.score += 1

            if self.masterServer != None:
                self.masterServer.reportGameEvent(self, enums.gameCommands.SetProperty, {"property": "score", "op": "inc", "value": 1})
                self.masterServer.reportGameEvent(self, enums.gameCommands.CallMethod, {"method": "_incTail", "pars": {"x": x, "y": y, "lastTailPiece": lastTailPiece}})

    def _incTail(self, x, y, lastTailPiece):
        self.world[y, x] = lastTailPiece