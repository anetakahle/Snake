from modules.agents import agentHuman


def setupClientHuman():
   humanClient = clientHuman.AgentHuman()
   humanClient.init()

def main():
   setupClientHuman()

main()