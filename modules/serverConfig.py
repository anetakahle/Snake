from modules import enums

class ServerConfig():

    # properties --------------
    mode = enums.serverModes.Manual
    gamesToPlay = 1
    fpsCallback = lambda x: False,
    newGameCallback = lambda x: False
    limitMovesPerGame = 1000
    masterServer = None

    # ctor ----------

    def __init__(self, mode = enums.serverModes.Manual, gamesToPlay = 1, fpsCallback = lambda x: False, newGameCallback = lambda x: False, limitMovesPerGame = 10000, masterServer = None):
        self.mode = mode
        self.gamesToPlay = gamesToPlay
        self.fpsCallback = fpsCallback
        self.newGameCallback = newGameCallback
        self.limitMovesPerGame = limitMovesPerGame
        self.masterServer = masterServer

defaultConfig = ServerConfig()