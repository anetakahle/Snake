import modules.gameCommand as gameCommand
import modules.enums as enums

class GameReport:

    # properties ------------

    commands : list[gameCommand.GameCommand] = []
    score : int = 0
    movesCount : int = 0
    server = None

    # ctor ------------

    def __init__(self, server):
        self.commands = []
        self.score = 0
        self.movesCount = 0
        self.server = server

    # public ----------------

    def addCommand(self, command : enums.gameCommands, data : {}):
        self.commands.append(gameCommand.GameCommand(command, data))

    def setScore(self, score : int):
        self.score = score

    def setMovesCount(self, movesCount : int):
        self.movesCount = movesCount