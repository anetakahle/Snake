from modules.clients import clientGenetic
import modules.masterServer as masterServer
import modules.clients.base.clientAiBase as cib
import modules.clients.base.clientAiBaseConfig as cibCfg
import modules.db.dbcontext as db
import modules.clients.clientGenetic2 as clientGenetic2

generations = 100
agents = 10
master = masterServer.MasterServer()

for gen in range(generations):

    # zapiseme info do dict, key = genindex, val = server.reporter/gameReporteret ... mnozina agentu, kteri hrali se stejnymi vahami
    for agent in range(agents):
        agent = clientGenetic.ClientGenetic(cibCfg.ClientAiBaseConfig(master, 10, agentIndex=agent, genIndex=gen, agentsCount = agents))

    master.start()
    master.serialize()
    print("generace: " + str(gen))
    print("top prumer: " + str(master.orderServerReportersByScore()[0].gamesAvgScore))
    master.stashGeneration(gen) #vyprazdneni
u =9