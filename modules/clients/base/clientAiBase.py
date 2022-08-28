import pygame

import modules.clients.base.clientBase as cb
import modules.enums as enums
import modules.renderCallback as rndrCb
import modules.server as srvr
import modules.render as rndr
import modules.serverConfig as serverConfig
from abc import ABC, abstractmethod
import modules.clients.base.clientAiBaseConfig as clientAiBaseConfig
import modules.db.dbcontext as db
import modules.serverReporter as serverReporter

class ClientAiBase(ABC, cb.ClientBase):

    # properties --------------

    enableRender = True
    server = object
    render = object
    actionsPerSecond = 1
    maxFramesIdle = 0
    currentFramesIdle = 0
    movementMode = enums.movementModes.Ai
    config : clientAiBaseConfig.ClientAiBaseConfig = None
    tickFn = None
    genId : int = 0
    agentId : int = 0
    genIndex : int = 0
    hiddenLayers = []

    # ctor --------------

    def __init__(self, config = clientAiBaseConfig.defaultClientAiBaseConfig):
        self.config = config
        self.genIndex = config.agentIndex
        self.server = srvr.Server(self, serverConfig.ServerConfig(masterServer = config.masterServer, gamesToPlay = config.gamesToPlay, limitMovesPerGame = config.maxMoves))
        self.init()
        self.setupLayers()

        if self.config.masterServer is None:
            renderCallback = rndrCb.RenderCallback(self.frameCallback, self.inputCallback)
            self.render = rndr.Render(self.server, enums.renderModes.PyGame, renderCallback)
            self.maxFramesIdle = self.render.fps / self.actionsPerSecond
            self.render.render()
        else:
            self.genId = db.insertGetId(f"""
                insert into ClientGenerations (clientId, "index") 
                values ({self.dbId}, {self.genIndex})
            """)[0]

            self.server.setMasterServer(self.config.masterServer)

            if self.config.masterServer.isGenerationStashed(self.genIndex - 1):
                self.mixLayers(self.config.masterServer.getStashedGeneration(self.genIndex - 1), self.config.agentIndex, self.config.agentsCount)

            self.server.setTickFn(self.frameCallback)
            renderCallback = rndrCb.RenderCallback(self.frameCallback, self.inputCallback)
            self.render = rndr.Render(self.server, enums.renderModes.Dormant, renderCallback)

    # public ----------------

    @abstractmethod
    def getFitness(self) -> int :
        pass

    @abstractmethod
    def mixLayers(self, prevGen : list[serverReporter.ServerReporter], clientIndex : int, clientsCount : int):
        pass

    @abstractmethod
    def setupLayers(self):
        pass

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def onFrame(self):
        pass

    @abstractmethod
    def brain(self) -> enums.directions :
        return enums.directions.Forward

    def postBrain(self):
        pass

    def frameCallback(self) -> bool:

        self.onFrame()

        if self.movementMode == enums.movementModes.Ai:
            self.currentFramesIdle += 1

            if self.currentFramesIdle > self.maxFramesIdle and self.server.isGameRunning():
                self.server.step(self.brain())
                self.currentFramesIdle = 0
                self.postBrain()
        return True

    def inputCallback(self, event):

        if self.movementMode == enums.movementModes.Human:
            if event.key == pygame.K_w:
                self.server.step(enums.directions.Forward)
            elif event.key == pygame.K_d:
                self.server.step(enums.directions.Right)
            elif event.key == pygame.K_a:
                self.server.step(enums.directions.Left)

            self.brain()
            self.postBrain()

        if event.key == pygame.K_SPACE:
            if self.movementMode == enums.movementModes.Ai:
                self.movementMode = enums.movementModes.Human
            else:
                self.movementMode = enums.movementModes.Ai

        if event.key == pygame.K_q:
            self.setupLayers()

    def serialize(self) -> int:
        return db.insertGetId(f"""
            insert into ClientGenerationAgents (runtimeId, clientGenerationId) 
            values ('{self.runtimeId}', {self.genId})
        """)[0]