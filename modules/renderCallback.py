class RenderCallback:
    # properties -----------

    fpsCallback = lambda x: True
    inputCallback = lambda x: True

    # ctor -------------

    def __init__(self, continueCallback, inputCallback):
        self.fpsCallback = continueCallback
        self.inputCallback = inputCallback