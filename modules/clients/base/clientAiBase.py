import pygame

import modules.clients.base.clientBase as cb
import modules.enums as enums
import modules.renderCallback as rndrCb
import modules.server as srvr
import modules.render as rndr
from abc import ABC, abstractmethod

class ClientAiBaseConfig:

    # properties ----------------

    masterServer = None
    gamesToPlay = 0

    # ctor --------------------

    def __init__(self, masterServer = None, gamesToPlay = 0):
        self.masterServer = masterServer
        self.gamesToPlay = gamesToPlay



defaultClientAiBaseConfig = ClientAiBaseConfig()

class ClientAiBase(ABC, cb.ClientBase):

    # properties --------------

    enableRender = True
    server = object
    render = object
    actionsPerSecond = 1
    maxFramesIdle = 0
    currentFramesIdle = 0
    movementMode = enums.movementModes.Ai
    config : ClientAiBaseConfig = None
    tickFn = None

    # ctor --------------

    def __init__(self, config = defaultClientAiBaseConfig):
        self.config = config
        self.server = srvr.Server()
        self.server.config.gamesToPlay = config.gamesToPlay
        self.init()
        self.setupLayers()

        if self.enableRender and self.config.masterServer == None:
            renderCallback = rndrCb.RenderCallback(self.frameCallback, self.inputCallback)
            self.render = rndr.Render(self.server, enums.renderModes.PyGame, renderCallback)
            self.maxFramesIdle = self.render.fps / self.actionsPerSecond
            self.render.render()

        if self.config.masterServer != None:
            self.server.setMasterServer(self.config.masterServer)
            self.server.setTickFn(self.frameCallback)


    # public ----------------

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

            if self.currentFramesIdle > self.maxFramesIdle:
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