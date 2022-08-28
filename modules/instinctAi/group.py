import modules.instinctAi.connection as connection


class Group:
    # properties ------------

    nodes : list = []
    connectionsIn : list[connection.Connection] = []
    connectionsOut : list[connection.Connection] = []
    connectionsSelf : list[connection.Connection] = []

    # ctor ---------------

    def __init__(self, size : int):
        import modules.instinctAi.node as node
        self.nodes = []
        self.connectionsIn = []
        self.connectionsOut = []
        self.connectionsSelf = []

        for i in range(size):
            self.nodes.append(node.Node())
