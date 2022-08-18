import modules.gameCommand as gameCommand
import modules.enums as enums

class GameReport:

    # properties ------------

    commands : list[gameCommand.GameCommand] = []

    # ctor ------------

    def __init__(self):
        pass

    # public ----------------

    def addCommand(self, command : enums.gameCommands, data : {}):
        self.commands.append(gameCommand.GameCommand(command, data))