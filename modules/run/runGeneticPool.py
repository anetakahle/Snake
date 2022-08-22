from modules.clients import clientGenetic
import modules.masterServer as masterServer
import modules.clients.base.clientAiBase as cib
import modules.clients.base.clientAiBaseConfig as cibCfg
import modules.db.dbcontext as db

generations = 10
agents = 10
master = masterServer.MasterServer()

for gen in range(generations):

    #modify gen
    pass

    # zapiseme info do dict, key = genindex, val = server.reporter/gameReporteret ... mnozina agentu, kteri hrali se stejnymi vahami

for agent in range(agents):
    agent = clientGenetic.ClientGenetic(cibCfg.ClientAiBaseConfig(master, 10, agentIndex=agent, genIndex=gen))

master.start()
games = master.orderGamesByScore()
bestServers = master.orderServersByScore()
master.serialize()
u =9