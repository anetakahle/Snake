from modules.clients import clientGenetic
import modules.masterServer as masterServer
import modules.clients.base.clientAiBase as cib

n = 100
master = masterServer.MasterServer()

for i in range(n):
    agent = clientGenetic.ClientGenetic(cib.ClientAiBaseConfig(master, 10))

master.start()

u = 0