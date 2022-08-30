import modules.agents.base.agentAiBaseConfig as cibCfg
import modules.agents.agentGenetic1Layer as agentGenetic1Layer
import modules.utils.iterable as iterable
import modules.agents.agentInstinct as agentInstinct
import modules.instinctAi.instinct as instinct
import modules.instinctAi.network as network

# generations = 1
agents = 1
instinctInst = instinct.Instinct(16, 3, agents, 20, 0.5, 3)
agentIndex = 0
agentInstinct.AgentInstinct(instinctInst, instinctInst.population[agentIndex], cibCfg.AgentAiBaseConfig(None, 1, agentIndex=0, genIndex=0, agentsCount = agents))

bp = 0