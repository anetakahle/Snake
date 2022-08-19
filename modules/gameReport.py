import modules.gameCommand as gameCommand
import modules.enums as enums

class GameReport:

    # properties ------------

    commands : list[gameCommand.GameCommand] = []
    score : int = 0

    # ctor ------------

    def __init__(self):
        self.commands = []
        self.score = 0

    # public ----------------

    def addCommand(self, command : enums.gameCommands, data : {}):
        self.commands.append(gameCommand.GameCommand(command, data))

    def setScore(self, score : int):
        self.score = score