from modules.clients import clientHuman


def setupClientHuman():
   humanClient = clientHuman.ClientHuman()
   humanClient.init()

def main():
   setupClientHuman()

main()