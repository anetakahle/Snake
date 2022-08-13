import modules.server as srvr
import modules.render as rndr
import modules.enums as enums
import modules.renderCallback as rndrCb
import modules.clientBase as cb
import pygame

class ClientHuman(cb.ClientBase):

    # properties ------------
    server = object

    # ctor -----------

    def init(self):
        renderCallback = rndrCb.RenderCallback(self.frameCallback, self.inputCallback)
        self.server = srvr.Server()
        render = rndr.Render(self.server, enums.renderModes.PyGame, renderCallback)
        render.render()

    # public ------------

    def frameCallback(self):
        return True

    def inputCallback(self, event):
        if event.key == pygame.K_w:
            self.server.step(enums.directions.Forward)
        elif event.key == pygame.K_d:
            self.server.step(enums.directions.Right)
        elif event.key == pygame.K_a:
            self.server.step(enums.directions.Left)