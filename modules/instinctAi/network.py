from __future__ import annotations
from typing import TYPE_CHECKING
import modules.instinctAi.node as node
import modules.instinctAi.connection as connection
import modules.instinctAi.instinct as instinct
import random
import modules.enums as enums
import math as math

class Network:

    # properties --------------

    inputSize : int
    outputSize : int
    nodes : list[node.Node]
    connections : list[connection.Connection]
    gates : list[connection.Connection]
    selfConnections : list[connection.Connection]
    dropout : int = 0
    score : int = 0
    population : list[Network] = []

    # ctor --------------------

    def __init__(self, inputSize : int, outputSize : int, score : int):
        self.inputSize = inputSize
        self.outputSize = outputSize
        self.nodes = []
        self.connections = []
        self.gates = []
        self.selfConnections = []
        self.dropout = 0
        self.score = score
        self.population = []

        for i in range(inputSize + outputSize):
            self.nodes.append(node.Node(enums.nodeTypes.Input if i < inputSize else enums.nodeTypes.Output))

        for i in range(inputSize):
            for j in range(inputSize, inputSize + outputSize):
                weight = random.random() * inputSize * math.sqrt(2 / inputSize)
                self.connect(self.nodes[i], self.nodes[j], weight)

    # public -------------------

    def activate(self, input : list[float], training : bool = False) -> list[float]:
        output = []
        index = 0

        for node in self.nodes:
            if node.type == enums.nodeTypes.Input:
                node.activate(input[index])
            elif node.type == enums.nodeTypes.Output:
                output.append(node.activate())
            else:
                if training:
                    node.mask = 0 if random.random() < self.dropout else 1
                node.activate()
            index += 1

        return output

    def connect(self, fromNode : node.Node, toNode : node.Node, weight : float) -> list[connection.Connection]:
        connections = fromNode.connect(toNode, weight)
        fromIsNotTo = fromNode is not toNode

        for conn in connections:
            if fromIsNotTo:
                self.connections.append(conn)
            else:
                self.selfConnections.append(conn)

        return connections

    def updateScore(self, scoreInc : int):
        self.score += scoreInc

    # private ----------------------
