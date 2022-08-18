import random

import modules.render as rndr
import modules.renderCallback as rndrCb
import modules.clients.base.clientBase as cb


class ClientGenetic(cb.ClientBase):

    # properties ------------
    server = object
    render = object
    actionsPerSecond = 10
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

    def brain(self):
        if self.server.scanDirEq(enums.directions.Left, enums.gameObjects.Apple):
            self.server.step(enums.directions.Left)
            return
        elif self.server.scanDirEq(enums.directions.Right, enums.gameObjects.Apple):
            self.server.step(enums.directions.Right)
            return
        elif self.server.scanDirEq(enums.directions.Forward, enums.gameObjects.Apple):
            self.server.step(enums.directions.Forward)
            return

        if self.server.scanDirBlocked(enums.directions.Forward):
            if self.server.scanDirBlocked(enums.directions.Right):
                self.server.step(enums.directions.Left)
                return
            elif self.server.scanDirBlocked(enums.directions.Left):
                self.server.step(enums.directions.Right)
                return
            self.server.step(random.choice([enums.directions.Left, enums.directions.Right]))
            return

        possibleActions = [enums.directions.Forward]
        if not self.server.scanDirBlocked(enums.directions.Right):
            possibleActions.append(enums.directions.Right)
        if not self.server.scanDirBlocked(enums.directions.Left):
            possibleActions.append(enums.directions.Left)
        self.server.step(random.choice(possibleActions))

    def frameCallback(self):

        self.currentFramesIdle += 1

        if self.currentFramesIdle > self.maxFramesIdle:
            self.brain()
            self.currentFramesIdle = 0

        return True

    def inputCallback(self, event):
        pass


#import tensorflow as tf
#from tensorflow.python.keras.layers import Dense
#from tensorflow.python.keras.models import Sequential
#from tensorflow.python.keras.optimizer_v2.adam import Adam
import numpy as  np
from modules import serverConfig as sc, server as srvr, enums
from modules.clients.base import clientBase as cb
from modules.GeneticAI import Activation_ReLU as relu, Dense_Layer as denl


class ClientGenetic(cb.ClientBase):

    # properties ------------
    server = object
    inputLayer = np.zeros(1)

    # ctor -----------

    def init(self):
        self.server = srvr.Server(sc.ServerConfig(enums.serverModes.Auto, 1, self.fpsCallback, self.newGameCallback, 10000))

    # public ------------

    def fpsCallback(self, movesRemaining):
        print(movesRemaining)

        return enums.directions.Skip

    def newGameCallback(self, gamesRemaining):
        pass

    # private ------------

    def preprocess_state(self):  # world and look_dir could be parameters
        # finding look_dir in order to know which objects are on our right etc.
        head = None
        neck = None
        body = None
        tail = None
        tail_value = 0
        world = server.getGameState().world
        size = server.getGameState().width
        for y in range(size):
            for x in range(size):
                if world[y][x] == 1:
                    head = [y, x]
                    world[y][x] += 1
                elif world[y][x] == 2:
                    neck = [y, x]
                    world[y][x] += 1
                elif world[y][x] > 2:
                    body = [y, x]
                    world[y][x] += 1
                if world[y][x] > tail_value:
                    tail = [y, x]
                    tail_value = world[y][x]

        y = head[0] - neck[0]
        x = head[1] - neck[1]
        look_dir = [y, x]

        look_dirs = [[0, -1], [-1, 0], [0, 1], [1, 0]]
        look_dir_index = look_dirs.index(look_dir)
        info_left = []
        indices_left = []  # actually its positions
        info_straight = []
        indices_straight = []
        info_right = []
        indices_right = []

        for ii in range(1, 4):
            shift_left = look_dirs[look_dir_index - 1]
            pixel_left_y = head[0] + ii * (shift_left[0])
            pixel_left_x = head[1] + ii * (shift_left[1])
            if (pixel_left_x > size - 1) or (pixel_left_y > size - 1) or (pixel_left_x < 0) or (
                    pixel_left_y < 0):  # if we can still move
                info_left.append(-2)
                indices_left.append(ii)
                break
            if world[pixel_left_y][pixel_left_x] != 0:
                info_left.append(world[pixel_left_y][pixel_left_x])
                indices_left.append(ii)

        for ii in range(1, 4):
            shift_straight = look_dirs[look_dir_index]
            pixel_straight_y = head[0] + ii * (shift_straight[0])
            pixel_straight_x = head[1] + ii * (shift_straight[1])
            if (pixel_straight_x > size - 1) or (pixel_straight_y > size - 1) or (pixel_straight_x < 0) or (
                    pixel_straight_y < 0):  # if we can still move
                info_straight.append(-2)
                indices_straight.append(ii)
                break
            if world[pixel_straight_y][pixel_straight_x] != 0:
                info_straight.append(world[pixel_straight_y][pixel_straight_x])
                indices_straight.append(ii)

        for ii in range(1, 4):
            if look_dir_index == 3:
                shift_right = look_dirs[0]
            else:
                shift_right = look_dirs[look_dir_index + 1]
            pixel_right_y = head[0] + ii * (shift_right[0])
            pixel_right_x = head[1] + ii * (shift_right[1])
            if (pixel_right_x > size - 1) or (pixel_right_y > size - 1) or (pixel_right_x < 0) or (
                    pixel_right_y < 0):  # if we can still move
                info_right.append(-2)
                indices_right.append(ii)
                break
            if world[pixel_right_y][pixel_right_x] != 0:
                info_right.append(world[pixel_right_y][pixel_right_x])
                indices_right.append(ii)

        if len(indices_left) != 0:
            input_layer[0] = 1 if ((indices_left[0] == 1) and (
                        (info_left[0] > 1 and info_left[0] != tail_value) or info_left[
                    0] == -2)) else 0  # there is an obsticle on the left (distance 1)
        if len(indices_straight) != 0:
            input_layer[1] = 1 if ((indices_straight[0] == 1) and (
                        (info_straight[0] > 1 and info_straight[0] != tail_value) or info_straight[0] == -2)) else 0
        if len(indices_right) != 0:
            input_layer[2] = 1 if ((indices_right[0] == 1) and (
                        (info_right[0] > 1 and info_right[0] != tail_value) or info_right[0] == -2)) else 0
        input_layer[3] = 1 if (-1 in info_left) else 0  # food in range 3 to the right
        input_layer[4] = 1 if (-1 in info_straight) else 0
        input_layer[5] = 1 if (-1 in info_right) else 0

        return input_layer


def onehot_encode(index, length):
    a = np.zeros((length,), dtype=np.uint8)
    a[index] = 1
    return a



X = preprocess_state(GameState.world) #instead of obs


dense1 = denl.Layer_Dense(6, 5)

activation1 = relu.Activation_ReLU()
#print(activation1.output)

dense1.forward(X)
#print(dense1.output)

activation1.forward(dense1.output)

print(activation1.output[:5])



#
# layer2 = Layer_Dense(5, 3)
#
#
# print(layer1)
# layer2.forward(layer1.output)
# print(layer2.output)


# In[ ]:





# In[ ]:


#output 2. vrstvy
#plan:
#batches neresime, 2 dense layers, vahy random, aktivacni fce, input, output
