import uuid
import modules.gameReporter as gameReport
import modules.server as server
import modules.utils.iterable as iterable

class ServerReporter:

    # properties --------------

    games : dict[uuid.UUID, gameReport.GameReporter] = {}
    currentGameId : uuid.UUID
    name = None
    server : server = None
    gamesAvgScore : float = 0.0

    # ctor -----------------

    def __init__(self, server):
        self.games = {}
        self.currentGameId = None
        self.name = uuid.uuid4()
        self.server = server
        self.gamesAvgScore = 0.0

    # public ----------------

    def enlistGame(self, gameId : uuid.UUID):
        self.games[gameId] = gameReport.GameReporter(self.server)
        self.currentGameId = gameId

    def getGamesScoreAvg(self) -> float :
        avgScore = iterable.avg([x.score for x in self.games.values()])
        self.gamesAvgScore = avgScore
        return avgScore

