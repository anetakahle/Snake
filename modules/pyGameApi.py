import pygame
import modules.enums as enums

class PyGameApi:
    # properties -----------------
    render = object
    font = object
    ds = object

    # ctor -------------

    def __init__(self, render, renderMode : enums.renderModes):
        self.render = render
        self.ds = render.ds

        if renderMode == enums.renderModes.PyGame:
            self.font = pygame.font.Font(pygame.font.get_default_font(), render.fs)

        return

    # public ---------------

    def drawLine(self, c, x1, y1, x2, y2, w=1):
        pygame.draw.line(self.ds, c, (x1, y1), (x2, y2), w)

    def drawPoly(self, c, vert):
        pygame.draw.polygon(self.ds, c, vert)

    def drawQuad(self, c, x1, y1, x2, y2, x3, y3, x4, y4):
        pygame.draw.polygon(self.ds, c, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])

    def drawTriangle(self, c, x1, y1, x2, y2, x3, y3):
        pygame.draw.polygon(self.ds, c, [(x1, y1), (x2, y2), (x3, y3)])

    def drawRect(self, c, x, y, w, h):
        pygame.draw.rect(self.ds, c, pygame.Rect(x, y, w, h))

    def drawRectExt(self, c, x, y, w, h, ow):
        pygame.draw.rect(self.ds, c, pygame.Rect(x, y, w, h), ow)

    def drawText(self, c, x, y, t):
        ts = self.font.render(t, True, c)
        self.ds.blit(ts, (x, y))

    def drawCircle(self, c, x, y, r):
        pygame.draw.circle(self.ds, c, (x, y), r / 2)

    def clear(self):
        self.drawRect(self.render.clrV, 0, 0, self.render.w, self.render.h)