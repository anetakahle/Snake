import uuid
import modules.gameReport as gameReport

class ServerReport:

    # properties --------------

    games : dict[uuid.UUID, gameReport.GameReport] = {}
    currentGameId : uuid.UUID
    name = None

    # ctor -----------------

    def __init__(self):
        self.games = {}
        self.currentGameId = None
        self.name = uuid.uuid4()

    # public ----------------

    def enlistGame(self, gameId : uuid.UUID):
        self.games[gameId] = gameReport.GameReport()
        self.currentGameId = gameId

