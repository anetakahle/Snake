from modules import enums, pyGameApi as pga
import pygame


class Render:

    # properties ----------
    server = object
    renderMode = enums.renderModes.PyGame
    inputMode = enums.inputModes.Hook
    logList = []
    s = 80  # cell size in px
    b = 0  # border size in px
    rl = True  # render log or not
    rg = True  # render grid or not
    rs = True  # render score or not
    fs = 26  # font size
    fps = 60  # target frames per second
    clrV = (0, 0, 0)  # void (background)
    clrA = (255, 0, 0)  # apple
    clrH = (0, 255, 0)  # head
    clrB = (0, 255, 0)  # body
    clrF = (255, 255, 255)  # foreground
    clrG = (40, 40, 40)  # grid
    queS = 5  # seconds to poll moves when input mode is set to "hook"
    draw = object

    # computed
    c = 8
    w = c * s
    h = c * s
    oq = s / 4
    oh = s / 2
    queF = fps * queS
    queC = 0
    if rl:
        w += s * 8

    ds = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()
    logList = []
    maxVal = 0
    stepQ = []
    run = True
    callbacks = object

    # ctor ----------

    def __init__(self, server, renderMode, callbacks):
        pygame.init()
        self.server = server
        self.renderMode = renderMode
        self.callbacks = callbacks
        self.draw = pga.PyGameApi(self)

    # public ------------

    def render(self):

        if self.server.getGameState().gameState == enums.gameStates.NotStarted:
            self.server.init()

        while self.run:
            if not self.callbacks.fpsCallback():
                self.run = False
                break

            self.clock.tick(self.fps)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    self.run = False
                elif e.type == pygame.KEYDOWN:
                    self.callbacks.inputCallback(e)

            self._render()
            pygame.display.update()

    def log(self, text, type = enums.logTypes.Info):
        self.logList.append([str(text), type])

    # private ----------

    def _renderPyGame(self):
        self.draw.clear()

        if self.rg:
            self._renderGrid()

        if self.rl:
            self.draw.drawRectExt(self.clrF, self.w / 2, 0, self.w / 2, self.h, 1)

        xx = 0
        yy = 0
        for y in self._getGameWorld():
            for x in y:
                self._cell(xx, yy, x)
                xx += 1
            yy += 1
            xx = 0
        self._renderLogList()

        if self.rs:
            self._renderScore()

    def _initRender(self):
        if self.renderMode == enums.renderModes.PyGame:
            pygame.init()

    def _render(self):
        if self.renderMode == enums.renderModes.PyGame:
            self._renderPyGame()

    def _getMaxVal(self):
        m = 0


        self.server.getGameState().iterateWorld()
        for y in self._getGameWorld():
            for x in y:
                if x > m:
                    m = x
        return m

    def _getValIndex(self, val):
        index = 0
        for y in self._getGameWorld():
            for x in y:
                if x == val:
                    return index
                index += 1
        return -1

    def _getValPos(self, val):
        index = self._getValIndex(val)
        c = self.server.getGameState().width
        self.log(index)
        if index == -1:
            return [-1, -1]
        yP = index // c
        xP = index - yP * c
        self.log("xp: " + str(xP) + " yp:" + str(yP))
        return [xP, yP]

    def _orient(self, xP, yP, val):
        pp = self._getValPos(val - 1)
        pn = self._getValPos(val + 1)
        isMax = val == self._getMaxVal()
        s, oh, oq = self.s, self.oh, self.oq

        #self.log("jsem blok: " + str(val) + " pp: " + str(pp) + " pn:" + str(pn) + " jsem posledni: " + str(isMax))
        if pp[0] == -1:
            return False
        if pp[0] - 1 == xP and pp[1] == yP:
            if isMax:
                self.draw.drawTriangle(self.clrB, (xP + 1) * s, yP * s + oq, (xP + 1) * s, yP * s + oh + oq, xP * s, yP * s + oh)
            else:
                if pn[0] != -1:
                    if pn[1] == yP + 1:
                        self.draw.drawRect(self.clrB, xP * s + oq, yP * s + oq, s - oq, oh)
                        self.draw.drawRect(self.clrB, xP * s + oq, yP * s + oq + oh, oh, oq)
                        return True
                    elif pn[1] == yP - 1:
                        self.draw.drawRect(self.clrB, xP * s + oq, yP * s + oq, s - oq, oh)
                        self.draw.drawRect(self.clrB, xP * s + oq, yP * s, oh, oq)
                        return True
                self.draw.drawRect(self.clrB, xP * s, yP * s + oq, s, oh)
            return True
        if pp[0] + 1 == xP and pp[1] == yP:
            if isMax:
                self.draw.drawTriangle(self.clrB, xP * s, yP * s + oq, xP * s, yP * s + oh + oq, (xP + 1) * s, yP * s + oh)
            else:
                if pn[0] != -1:
                    if pn[1] == yP + 1:
                        self.draw.drawRect(self.clrB, xP * s, yP * s + oq, s - oq, oh)
                        self.draw.drawRect(self.clrB, xP * s + oq, yP * s + oq + oh, oh, oq)
                        return True
                    elif pn[1] == yP - 1:
                        self.draw.drawRect(self.clrB, xP * s, yP * s + oq, s - oq, oh)
                        self.draw.drawRect(self.clrB, xP * s + oq, yP * s, oh, oq)
                        return True
                self.draw.drawRect(self.clrB, xP * s, yP * s + oq, s, oh)
            return True
        if pp[0] == xP and pp[1] - 1 == yP:
            if isMax:
                self.draw.drawTriangle(self.clrB, xP * s + oq, (yP + 1) * s, xP * s + oh + oq, (yP + 1) * s, xP * s + oh, yP * s)
            else:
                if pn[0] != -1:
                    if pn[0] == xP - 1:
                        self.draw.drawRect(self.clrB, xP * s + oq, yP * s + oq, oh, s - oq)
                        self.draw.drawRect(self.clrB, xP * s, yP * s + oq, oq, oh)
                        return True
                    elif pn[0] == xP + 1:
                        self.draw.drawRect(self.clrB, xP * s + oq, yP * s + oq, oh, s - oq)
                        self.draw.drawRect(self.clrB, xP * s + oh + oq, yP * s + oq, oq, oh)
                        return True
                self.draw.drawRect(self.clrB, xP * s + oq, yP * s, oh, s)
            return True
        if pp[0] == xP and pp[1] + 1 == yP:
            if isMax:
                self.draw.drawTriangle(self.clrB, xP * s + oq, yP * s, xP * s + oh + oq, yP * s, xP * s + oh, (yP + 1) * s)
            else:
                if pn[0] != -1:
                    if pn[0] == xP - 1:
                        self.draw.drawRect(self.clrB, xP * s + oq, yP * s, oh, s - oq)
                        self.draw.drawRect(self.clrB, xP * s, yP * s + oq, oq, oh)
                        return True
                    elif pn[0] == xP + 1:
                        self.draw.drawRect(self.clrB, xP * s + oq, yP * s, oh, s - oq)
                        self.draw.drawRect(self.clrB, xP * s + oh + oq, yP * s + oq, oq, oh)
                        return True
                self.draw.drawRect(self.clrB, xP * s + oq, yP * s, oh, s)
            return True
        return False

    def _cell(self, xP, yP, val):
        s, oh, oq = self.s, self.oh, self.oq
        if val == 0:
            return
        else:
            clr = self.clrA
            if val == -1:
                self.draw.drawCircle(clr, xP * self.s + self.oh, yP * self.s + self.oh, self.s)
                return
            if val == 1:
                pn = self._getValPos(val + 1)
                if pn[0] != -1:
                    ppp = 0
                    # if pn[0] == xP and pn[1] == yP - 1:
                    #     drawPoly(clrA, [
                    #         (xP * s + oq, (yP + 1) * s),
                    #         (xP * s, yP * s + oh),
                    #         (xP * s + oq, yP * s),
                    #         (yP * s + oq + oh, yP * s),
                    #         ((xP + 1) * s, yP * s + oh),
                    #         (xP * s + oq + oh, (yP + 1) * s),
                    #         (xP * s + oq, (yP + 1) * s)
                    #     ])
                    #     return
                clr = self.clrH
            elif val >= 2:
                clr = self.clrB
                t = self._orient(xP, yP, val)
                if t:
                    return
            self.draw.drawRect(clr, xP * s, yP * s, s, s)

    def _renderLogList(self):
        if not self.rl:
            return
        index = 0
        for entry in self.logList:
            c = self.clrF
            if entry[1] == enums.logTypes.Ok:
                c = (0, 255, 0)
            elif entry[1] == enums.logTypes.Warn:
                c = (255, 165, 0)
            elif entry[1] == enums.logTypes.Error:
                c = (255, 0, 0)
            self.draw.drawText(c, self.w / 2 + 10, 10 + index * (self.fs + 4), entry[0])
            index += 1
        self.logList = []

    def _getScore(self):
        return self.server.getGameState().score

    def _getGameWorld(self):
        return self.server.getGameState().world

    def _renderGrid(self):
        index = 0
        c = self.server.getGameState().width
        for _ in range(c):
            self.draw.drawLine(self.clrG, index * self.s, 0, index * self.s, self.s * c)
            self.draw.drawLine(self.clrG, 0, index * self.s, self.s * c, index * self.s)
            index += 1

    def _renderScore(self):
        self.draw.drawText(self.clrF, 6, 6, "Skore: " + str(self._getScore()))

