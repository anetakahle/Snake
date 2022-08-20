from modules.clients import clientGenetic
import modules.masterServer as masterServer
import modules.clients.base.clientAiBase as cib

n = 10
master = masterServer.MasterServer()

for i in range(n):
    agent = clientGenetic.ClientGenetic(cib.ClientAiBaseConfig(master, 10))

master.start()
games = master.orderByScore()
u = 0