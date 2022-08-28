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
    gamesAvgFitness : float = 0.0
    gamesMaxScore : int = 0
    gamesMaxFitness : int = 0

    # ctor -----------------

    def __init__(self, server):
        self.games = {}
        self.currentGameId = None
        self.name = uuid.uuid4()
        self.server = server
        self.gamesAvgScore = 0.0
        self.gamesAvgFitness = 0.0
        self.gamesMaxFitness = 0
        self.gamesMaxScore = 0

    # public ----------------

    def enlistGame(self, gameId : uuid.UUID):
        self.games[gameId] = gameReport.GameReporter(self.server)
        self.currentGameId = gameId

    def getGamesScoreAvg(self) -> float :
        source = [x.score for x in self.games.values()]
        avgScore = iterable.avg(source)
        maxScore = max(source)
        self.gamesAvgScore = avgScore
        self.gamesMaxScore = maxScore
        return avgScore

    def getGamesFitnessAvg(self) -> float :
        source = [x.fitness for x in self.games.values()]
        avgFitness = iterable.avg(source)
        maxFitness = max(source)
        self.gamesAvgFitness = avgFitness
        self.gamesMaxFitness = maxFitness
        return avgFitness

