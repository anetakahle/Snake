import modules.enums as enums

class GameCommand:

    # properties ------------

    cmd : enums.gameCommands = enums.gameCommands.Unknown
    data : {}

    # ctor ---------------

    def __init__(self, command : enums.gameCommands, data : dict):
        self.cmd = command
        self.data = data