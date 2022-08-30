import modules.agents.base.clientAiBaseConfig as cibCfg
import modules.agents.agentGenetic1Layer as clientGenetic1Layer
import modules.utils.iterable as iterable
import modules.agents.agentInstinct as clientInstinct
import modules.instinctAi.instinct as instinct
import modules.instinctAi.network as network

# generations = 1
agents = 1
instinctInst = instinct.Instinct(16, 3, agents, 20, 0.5, 3)
agentIndex = 0
clientInstinct.AgentInstinct(instinctInst, instinctInst.population[agentIndex], cibCfg.ClientAiBaseConfig(None, 1, agentIndex=0, genIndex=0, agentsCount = agents))

bp = 0