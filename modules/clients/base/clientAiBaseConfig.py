class ClientAiBaseConfig:

    # properties ----------------

    masterServer = None
    gamesToPlay = 0
    maxMoves = 1000
    dbId = 0
    genIndex : int = 0
    agentIndex : int = 0

    # ctor --------------------

    def __init__(self, masterServer = None, gamesToPlay = 0, maxMoves = 1000, dbId = 0, genIndex = 0, agentIndex = 0):
        self.masterServer = masterServer
        self.gamesToPlay = gamesToPlay
        self.maxMoves = maxMoves
        self.dbId = dbId
        self.genIndex = genIndex
        self.agentIndex = agentIndex




defaultClientAiBaseConfig = ClientAiBaseConfig()