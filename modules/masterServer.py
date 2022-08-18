import modules.server as server
import modules.serverReport as serverReport
import modules.enums as enums
import uuid


class MasterServer():

    # properties ------------------

    slaveServers = []
    slaveServersDict : dict[server.Server, serverReport.ServerReport] = {}
    running = False

    # ctor --------------

    def __init__(self):
        pass

    # public -----------------

    def reportNewGame(self, server : server.Server):
        gameId = self._getNextGameId()

        if server not in self.slaveServersDict:
            sr = serverReport.ServerReport()
            sr.enlistGame(gameId)
            self.slaveServersDict[server] = sr
        else:
            self.slaveServersDict[server].enlistGame(gameId)

    def reportGameEvent(self, server : server.Server, command : enums.gameCommands, data : {}):
        self.slaveServersDict[server].currentGameReport.addCommand(command, data)

    def reportEndGame(self, server : server.Server):
        self.slaveServersDict[server].currentGameReport.addCommand(enums.gameCommands.GameEnd, {})

    def enlistSlave(self, server : server.Server):
        self.slaveServers.append(server)
        self.slaveServersDict[server] = serverReport.ServerReport()

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