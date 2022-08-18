from modules import enums

class ServerConfig():

    # properties --------------
    mode = enums.serverModes.Manual
    gamesToPlay = 1
    fpsCallback = lambda x: False,
    newGameCallback = lambda x: False
    limitMovesPerGame = 10000

    # ctor ----------

    def __init__(self, mode = enums.serverModes.Manual, gamesToPlay = 1, fpsCallback = lambda x: False, newGameCallback = lambda x: False, limitMovesPerGame = 10000):
        self.mode = mode
        self.gamesToPlay = gamesToPlay
        self.fpsCallback = fpsCallback
        self.newGameCallback = newGameCallback
        self.limitMovesPerGame = limitMovesPerGame

defaultConfig = ServerConfig()