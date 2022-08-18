import uuid
import modules.gameReport as gameReport

class ServerReport:

    # properties --------------

    games : dict[uuid.UUID, gameReport.GameReport] = {}
    currentGameId : uuid.UUID = None
    currentGameReport : gameReport.GameReport = None

    # ctor -----------------

    def __init__(self):

        pass

    # public ----------------

    def enlistGame(self, gameId : uuid.UUID):
        self.currentGameReport = gameReport.GameReport()
        self.currentGameId = gameId

