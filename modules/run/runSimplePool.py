from modules.clients import clientGenetic
import modules.masterServer as masterServer
import modules.clients.base.clientAiBase as cib
import modules.clients.base.clientAiBaseConfig as cibCfg
import modules.db.dbcontext as db
import modules.clients.clientSimple as clientSimple
import modules.clients.clientRandom as clientRandom
import modules.utils.iterable as iterable

generations = 1
agents = 1
master = masterServer.MasterServer()

for gen in range(generations):

    # zapiseme info do dict, key = genindex, val = server.reporter/gameReporteret ... mnozina agentu, kteri hrali se stejnymi vahami
    for agent in range(agents):
        agent = clientSimple.ClientSimple(cibCfg.ClientAiBaseConfig(master, 10, 1, agentIndex=agent, genIndex=gen, agentsCount = agents))

    master.start()
    master.serialize()
    print("generace: " + str(gen))
    print("top prumer fitness: " + str(master.orderServerReportersByFitness()[0].gamesAvgFitness))
    print("top prumer skore: " + str(master.orderServerReportersByScore()[0].gamesAvgScore))

    master.stashGeneration(gen) #vyprazdneni

topScore = max([x.gamesMaxScore for x in [item for sublist in master.stashedServerReporters.values() for item in sublist]])

print("Celkove prumerne skore: " + str(iterable.avg([x.gamesAvgScore for x in [item for sublist in master.stashedServerReporters.values() for item in sublist]])))
print("Nejlepsi celkove skore: " + str(topScore))
bp = 0