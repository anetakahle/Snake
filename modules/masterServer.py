import uuid
from modules import server, serverReport, enums


class MasterServer():

    # properties ------------------

    slaveServers : dict[server.Server, serverReport.ServerReport] = {}
    running = False

    # ctor --------------

    def __init__(self):
        pass

    # public -----------------

    def enlistSlave(self, server : server.Server) -> bool:
        if server not in self.slaveServers:
            sr = serverReport.ServerReport()
            self.slaveServers[server] = sr
            return True
        return False

    def reportNewGame(self, server : server.Server) -> uuid.UUID:
        gameId = self._getNextGameId()

        if server not in self.slaveServers:
            sr = serverReport.ServerReport()
            self.slaveServers[server] = sr

        self.slaveServers[server].enlistGame(gameId)
        return gameId

    def reportGameEvent(self, server : server.Server, command : enums.gameCommands, data : {}):
        self.slaveServers[server].games[self.slaveServers[server].currentGameId].addCommand(command, data)

    def reportEndGame(self, server : server.Server):
        self.slaveServers[server].games[self.slaveServers[server].currentGameId].addCommand(enums.gameCommands.GameEnd, {})
        self.slaveServers[server].games[self.slaveServers[server].currentGameId].setScore(server.score)

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

    # private -------------------

    def _getNextGameId(self) -> uuid.UUID:
        return uuid.uuid4()