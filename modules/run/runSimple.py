from modules.clients import clientSimple
from modules.clients.base.clientAiBaseConfig import ClientAiBaseConfig

config = ClientAiBaseConfig(gamesToPlay=1, maxMoves=10)
agent = clientSimple.ClientSimple(config=config)
