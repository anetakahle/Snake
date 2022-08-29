from __future__ import annotations

import random

import modules.enums as enums
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import modules.instinctAi.node as node

class Connection:

    # properties -------------

    fromNode : node.Node = None
    toNode : node.Node = None
    weight : float = 0.0
    gater : node.Node = None
    gain : float = 0.0
    eligibility : float = 0.0
    previousDeltaWeight : float = 0.0
    totalDeltaWeight : float = 0.0
    xtraceNodes : list[node.Node]
    xtraceValues : list

    def __init__(self, fromNode : node.Node, toNode : node.Node, weight : float = None):
        self.fromNode = fromNode
        self.toNode = toNode
        self.weight = weight
        self.gater = None
        self.gain = 1.0
        self.eligibility = 0.0
        self.previousDeltaWeight = 0.0
        self.totalDeltaWeight = 0.0
        self.xtraceNodes = []
        self.xtraceValues = []

        if weight is None:
            self.weight = random.random() * 0.2 - 0.1