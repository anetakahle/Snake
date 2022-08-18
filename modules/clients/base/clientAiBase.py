import modules.clients.base.clientBase as cb
import modules.enums as enums
import modules.renderCallback as rndrCb
import modules.server as srvr
import modules.render as rndr
from abc import ABC, abstractmethod

class ClientAiBase(ABC, cb.ClientBase):

    # properties --------------

    enableRender = True
    server = object
    render = object
    actionsPerSecond = 1
    maxFramesIdle = 0
    currentFramesIdle = 0

    # ctor --------------

    def __init__(self):
        self.server = srvr.Server()

        if self.enableRender:
            renderCallback = rndrCb.RenderCallback(self.frameCallback, self.inputCallback)
            self.render = rndr.Render(self.server, enums.renderModes.PyGame, renderCallback)
            self.maxFramesIdle = self.render.fps / self.actionsPerSecond
            self.render.render()

    # public ----------------

    @abstractmethod
    def brain(self):
        return enums.directions.Forward

    def frameCallback(self):

        self.currentFramesIdle += 1

        if self.currentFramesIdle > self.maxFramesIdle:
            self.server.step(self.brain())
            self.currentFramesIdle = 0
        return True

    def inputCallback(self, event):
        pass