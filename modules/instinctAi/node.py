from __future__ import annotations
import modules.enums as enums
import modules.instinctAi.connection as connection
import modules.instinctAi.group as group
import modules.utils.iterable as iterable
import defaultlist as defaultlist

class NodeConnections:

    # properties ------------------------
    inNodes : list[connection.Connection] = []
    outNodes: list[connection.Connection] = []
    gatedNodes: list[connection.Connection] = []
    selfConnection : connection.Connection = None
    node : Node = None

    # ctor ------------------------

    def __init__(self, node : Node):
        self.node = node
        self.selfConnection = connection.Connection(node, node, 0)
        self.inNodes = []
        self.outNodes = []
        self.gatedNodes = []


class Node:

    # properties ------------

    connections : NodeConnections = None
    type : enums.nodeTypes = None
    activation : float = 0.0
    state : float = 0.0
    old : float = 0.0
    squash : enums.activationFunctions = enums.activationFunctions.Logistic
    mask = 1.0
    derivative : float = 0.0

    # ctor  -------------------------

    def __init__(self, type : enums.nodeTypes = enums.nodeTypes.Hidden):
        self.type = type
        self.connections = NodeConnections(self)
        self.activation = 0.0
        self.state = 0.0
        self.old = 0.0
        self.squash = enums.activationFunctions.Logistic
        self.mask = 1.0
        self.derivative = 0.0

    # public ----------------

    def activate(self, input : float = None) -> float :
        if input is not None:
            self.activation = input
            return input

        self.old = self.state
        self.state = self.connections.selfConnection.gain * self.connections.selfConnection.weight * self.state + self.bias

        for inConn in self.connections.inNodes:
            self.state += inConn.fromNode.activation * inConn.weight * inConn.gain

        self.activation = self.squash.Call(self.state, False) * self.mask
        self.derivative = self.squash.Call(self.state, True)

        nodes : list[Node] = []
        influences : list[float] = defaultlist.defaultlist()

        for gatedConn in self.connections.gatedNodes:
            index = iterable.indexOf(nodes, gatedConn.toNode)

            if index is not None:
                influences[index] += gatedConn.weight * gatedConn.fromNode.activation
            else:
                nodes.append(gatedConn.toNode)
                x = gatedConn.toNode.old if gatedConn.toNode.connections.selfConnection.gater is self else 0
                influences.append(gatedConn.weight * gatedConn.fromNode.activation + x)

            gatedConn.gain = self.activation

        for inConn in self.connections.inNodes:
            inConn.eligibility = self.connections.selfConnection.gain * self.connections.selfConnection.weight * inConn.eligibility + inConn.fromNode.activation * inConn.gain

            index = 0
            for node in nodes:
                influence = influences[index]
                jIndex = iterable.indexOf(inConn.xtraceNodes, node)

                if jIndex is not None:
                    inConn.xtraceValues[jIndex] = node.connections.selfConnection.gain * node.connections.selfConnection.weight * inConn.xtraceValues[jIndex] + self.derivative * inConn.eligibility * influence
                else:
                    inConn.xtraceNodes.append(node)
                    inConn.xtraceValues.append(self.derivative * inConn.eligibility * influence)

                index += 1

        return self.activation

    def warn(self, text : str):
        pass

    def isProjectingTo(self, node : Node) -> bool :
        if node is self and self.connections.selfConnection.weight != 0:
            return True
        for conn in self.connections.outNodes:
            if conn.toNode is node:
                return True
        return False

    def connectToGroup(self, target : group.Group, weight : float) -> list[connection.Connection] :
        connections = []

        for node in target.nodes:
            conn = connection.Connection(self, node, weight)
            node.connections.inNodes.append(conn)
            self.connections.outNodes.append(conn)
            target.connectionsIn.append(conn)
            connections.append(conn)

        return connections

    def connect(self, target : Node, weight : float) -> list[connection.Connection] :
        connections = []

        if target is self:
            if self.connections.selfConnection.weight is not 0:
                self.warn('This connection already exists!')
            else:
                self.connections.selfConnection.weight = weight or 1
            connections.append(self.connections.selfConnection)
        elif self.isProjectingTo(target):
            self.warn("Error : 'Already projecting a connection to this node!'")
        else:
            conn = connection.Connection(self, target, weight)
            target.connections.inNodes.append(conn)
            self.connections.outNodes.append(conn)
            connections.append(conn)

        return connections

    # private ------------------------

    def _setProperties(self):
        if self.type == enums.nodeTypes.Input:
            self.bias = 0
        else:
            self.bias = 0
