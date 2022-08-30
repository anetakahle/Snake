import modules.server as srvr
import modules.render as rndr
import modules.enums as enums
import modules.renderCallback as rndrCb
import modules.agents.base.clientBase as cb
import pygame

class AgentHuman(cb.ClientBase):

    # properties ------------
    server = object
    render = object

    # ctor -----------

    def init(self):
        renderCallback = rndrCb.RenderCallback(self.frameCallback, self.inputCallback)
        self.server = srvr.Server(self)
        self.render = rndr.Render(self.server, enums.renderModes.PyGame, renderCallback)
        self.render.render()

    # public ------------

    def frameCallback(self):

        self.render.log("Nalevo je: " + str(self.server.scanDir(enums.directions.Left, 1)), enums.logTypes.Warn)
        self.render.log("Rovne je: " + str(self.server.scanDir(enums.directions.Forward, 1)), enums.logTypes.Warn)
        self.render.log("Napravo je: " + str(self.server.scanDir(enums.directions.Right, 1)), enums.logTypes.Warn)

        return True

    def inputCallback(self, event):
        if event.key == pygame.K_w:
            self.server.step(enums.directions.Forward)
        elif event.key == pygame.K_d:
            self.server.step(enums.directions.Right)
        elif event.key == pygame.K_a:
            self.server.step(enums.directions.Left)