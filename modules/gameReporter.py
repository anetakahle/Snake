import modules.gameCommand as gameCommand
import modules.enums as enums
import modules.db.iSerializable as iSerializable
import modules.db.dbcontext as db
import modules.server as serverCls
import modules.utils.datetime2 as datetime2

class GameReporter(iSerializable.ISerializable):

    # properties ------------

    commands : list[gameCommand.GameCommand] = []
    score : int = 0
    movesCount : int = 0
    server : serverCls.Server = None
    agentId : int = 0
    clientId : int = 0
    fitness : int = 0

    # ctor ------------

    def __init__(self, server):
        self.commands = []
        self.score = 0
        self.movesCount = 0
        self.server = server
        self.clientId = server.client.dbId
        self.fitness = 0

    # public ----------------

    def addCommand(self, command : enums.gameCommands, data : {}):
        self.commands.append(gameCommand.GameCommand(command, data))

    def setFitness(self, fitness : int):
        self.fitness = fitness

    def setScore(self, score : int):
        self.score = score

    def setMovesCount(self, movesCount : int):
        self.movesCount = movesCount

    def serialize(self):
        self.agentId = self.server.client.serialize()

        db.execSql(f"""
            insert into Games (runtimeId, clientId, clientGenerationAgentId, data, dateStart, dateEnd, score, moves, endReason) 
            values ('', {self.clientId}, {self.agentId}, '', '{self.server.startTimeSql}', '{datetime2.sqlNow()}', {self.score}, {self.movesCount}, 0)
        """)