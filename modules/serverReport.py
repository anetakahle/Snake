import uuid
import modules.gameReport as gameReport
import modules.server as server

class ServerReport:

    # properties --------------

    games : dict[uuid.UUID, gameReport.GameReport] = {}
    currentGameId : uuid.UUID
    name = None
    server : server = None

    # ctor -----------------

    def __init__(self, server):
        self.games = {}
        self.currentGameId = None
        self.name = uuid.uuid4()
        self.server = server

    # public ----------------

    def enlistGame(self, gameId : uuid.UUID):
        self.games[gameId] = gameReport.GameReport(self.server)
        self.currentGameId = gameId

