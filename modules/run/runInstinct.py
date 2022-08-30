import modules.masterServer as masterServer
import modules.clients.base.clientAiBaseConfig as cibCfg
import modules.clients.clientGenetic1Layer as clientGenetic1Layer
import modules.utils.iterable as iterable
import modules.clients.clientInstinct as clientInstinct
import modules.instinctAi.instinct as instinct
import modules.instinctAi.network as network

generations = 10
agents = 10
master = masterServer.MasterServer()
popSize = 16

instinctInst = instinct.Instinct(popSize, 3, agents, 20, 0.5, 3, None, 0.2 * popSize)
agentIndex = 0

for gen in range(generations):

    agentIndex = 0

    for agent in range(agents):
        clientInstinct.ClientInstinct(instinctInst, instinctInst.population[agentIndex], cibCfg.ClientAiBaseConfig(master, 1, agentIndex=agent, genIndex=gen, agentsCount = agents))
        agentIndex += 1

    master.start()
    master.serialize()
    print("generace: " + str(gen))
    print("top prumer fitness: " + str(master.orderServerReportersByFitness()[0].gamesAvgFitness))
    print("top prumer skore: " + str(master.orderServerReportersByScore()[0].gamesAvgScore))


    master.stashGeneration(gen)

    instinctInst.sortPopulationByScore()

    newGen : list[network.Network] = []
    elites = []

    for i in range(instinctInst.elitism):
        elites.append(instinctInst.population[i])

    for i in range(popSize - instinctInst.elitism):
        newGen.append(instinctInst.getOffspring())



topScore = max([x.gamesMaxScore for x in [item for sublist in master.stashedServerReporters.values() for item in sublist]])

print("Celkove prumerne skore: " + str(iterable.avg([x.gamesAvgScore for x in [item for sublist in master.stashedServerReporters.values() for item in sublist]])))
print("Nejlepsi celkove skore: " + str(topScore))
bp = 0