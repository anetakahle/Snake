class RenderCallback:
    # properties -----------

    continueCallback = lambda x: True
    inputCallback = lambda x: True

    # ctor -------------

    def __init__(self, continueCallback, inputCallback):
        self.continueCallback = continueCallback
        self.inputCallback = inputCallback