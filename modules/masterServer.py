import uuid
from modules import server, serverReporter, enums, gameReporter
import modules.db.dbcontext as db
import modules.db.iSerializable as iSerializable
import modules.clients.base.clientAiBase as clientAiBase

class MasterServer(iSerializable.ISerializable):

    # properties ------------------

    slaveServers : dict[server.Server, serverReporter.ServerReporter] = {}
    running = False
    stashedServerReporters : dict[int, list[serverReporter.ServerReporter]] = {}

    # ctor --------------

    def __init__(self):
        self.slaveServers = {}
        self.running = False
        self.stashedServerReporters = {}
        pass

    # public -----------------

    def enlistSlave(self, server : server.Server) -> bool:
        if server not in self.slaveServers:
            sr = serverReporter.ServerReporter(server)
            self.slaveServers[server] = sr
            return True
        return False

    def reportNewGame(self, server : server.Server) -> uuid.UUID:
        gameId = self._getNextGameId()
        self.enlistSlave(server)

        self.slaveServers[server].enlistGame(gameId)
        return gameId

    def reportGameEvent(self, server : server.Server, command : enums.gameCommands, data : {}):
        self.slaveServers[server].games[self.slaveServers[server].currentGameId].addCommand(command, data)

    def reportEndGame(self, server : server.Server):
        self.slaveServers[server].games[self.slaveServers[server].currentGameId].addCommand(enums.gameCommands.GameEnd, {})
        self.slaveServers[server].games[self.slaveServers[server].currentGameId].setScore(server.score)
        self.slaveServers[server].games[self.slaveServers[server].currentGameId].setMovesCount(server.movesCount)

    def start(self):
        self.running = True
        while self.running:
            self.running = self.clock()

    def clock(self) -> bool:
        anyServerAccepted = False

        for server in self.slaveServers:
            accepted = server.dispatchClockFn()

            if not anyServerAccepted:
                anyServerAccepted = accepted

        return anyServerAccepted

    def getAllGames(self): #returns a list of games
        allGames = []
        for server in self.slaveServers.values(): #server reporters
            gamesList = list(server.games.values())
            allGames.extend(gamesList)

        return allGames

    def orderGamesByScore(self, desc : bool = True) -> list[gameReporter.GameReporter] :
        return sorted(self.getAllGames(), key=lambda x: x.score, reverse=desc)

    def serialize(self): # vsechny game reporteri napisou do tabulky vysledky
        for game in self.getAllGames():
            game.serialize()

    def orderServerReportersByScore(self, desc : bool = True) -> list[serverReporter.ServerReporter] :
        for slave in self.slaveServers.values():
            slave.getGamesScoreAvg()
        return sorted(self.slaveServers.values(), key=lambda x: x.gamesAvgScore, reverse=desc)

    def stashGeneration(self, genIndex : int):
        self.stashedServerReporters[genIndex] = self.orderServerReportersByScore()
        self.slaveServers = {}

    def getStashedGeneration(self, genIndex : int) -> list[serverReporter.ServerReporter] :
        return self.stashedServerReporters[genIndex]

    def isGenerationStashed(self, genIndex : int) -> bool :
        return genIndex in self.stashedServerReporters


    # private -------------------

    def _getNextGameId(self) -> uuid.UUID:
        return uuid.uuid4()


