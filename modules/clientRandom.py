import random

import modules.server as srvr
import modules.render as rndr
import modules.enums as enums
import modules.renderCallback as rndrCb
import modules.clientBase as cb
import pygame

class ClientRandom(cb.ClientBase):

    # properties ------------
    server = object
    render = object
    actionsPerSecond = 2
    maxFramesIdle = 0
    currentFramesIdle = 0

    # ctor -----------

    def init(self):
        renderCallback = rndrCb.RenderCallback(self.frameCallback, self.inputCallback)
        self.server = srvr.Server()
        self.render = rndr.Render(self.server, enums.renderModes.PyGame, renderCallback)
        self.maxFramesIdle = self.render.fps / self.actionsPerSecond
        self.render.render()

    # public ------------

    def frameCallback(self):

        self.currentFramesIdle += 1

        if self.currentFramesIdle > self.maxFramesIdle:
            self.server.step(random.choice([enums.directions.Forward, enums.directions.Right, enums.directions.Left]))
            self.currentFramesIdle = 0

        return True

    def inputCallback(self, event):
        pass