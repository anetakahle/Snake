#!/usr/bin/env python
# coding: utf-8

# # IMPORTS, INITIALIZATION

# In[1]:

GetGameState

SetGameState

import random
import math
import numpy as np
from matplotlib import pyplot as plt
# import pygame
from time import sleep

# In[2]:


# get_ipython().run_line_magic('env', 'QT_QPA_PLATFORM=wayland7')
# get_ipython().run_line_magic('matplotlib', 'tk')
global renderMode
global score
global obs
global extStep
extStep = -2


# In[2]:





# # SETUP

# In[3]:


size = 8
renderMode = 1


# In[3]:





# # GAME LOGIC

# In[4]:


env_state = 'open'
apple_collected = False

def reset_env():
    global obs
    obs = np.zeros((size, size), dtype=int)
    middle = [math.floor((size+1)/2)-1, math.ceil((size+1)/2)-1]
    y = random.randint(*middle)
    x = random.randint(*middle)
    obs[y][x] = 1 #head
    obs[y+1][x] = 2 #body
    return obs

def generate_apple():
    y = random.randint(0, size-1)
    x = random.randint(0, size-1)
    while obs[y, x] !=0:
        y = random.randint(0, size-1)
        x = random.randint(0, size-1)
    obs[y, x] = -1


def step(action):
    global apple_collected
    apple_collected = False
    tail_value = 0
    head = None
    global obs
    neck = None
    body = None
    tail = None
    for y in range(size):
        for x in range(size):
            if obs[y][x] == 1:
                head = [y, x]
                obs[y][x] += 1
            elif obs[y][x] == 2:
                neck = [y, x]
                obs[y][x] += 1
            elif obs[y][x] > 2:
                body = [y, x]
                obs[y][x] += 1
            if obs[y][x] > tail_value:
                tail = [y, x]
                tail_value = obs[y][x]
    #if tail is None:

    if_apple = obs[tail[0]][tail[1]]
    obs[tail[0]][tail[1]] = 0

    y = head[0]-neck[0]
    x = head[1]-neck[1]
    look_dir = [y, x]

    look_dirs = [[0, -1], [-1, 0], [0, 1], [1, 0]]
    look_dir_index = look_dirs.index(look_dir)
    head_movement = None

    if action == -1: #left
        head_movement = look_dirs[look_dir_index-1]
    elif action == 0: #straight
        head_movement = look_dirs[look_dir_index]
    elif action == 1: #right
        if look_dir_index == 3:
            head_movement = look_dirs[0]
        else:
            head_movement = look_dirs[look_dir_index+1]

    new_head_y = head[0]+head_movement[0]
    new_head_x = head[1]+head_movement[1]

    if (new_head_x > size-1) or (new_head_y > size-1) or (new_head_x < 0) or (new_head_y < 0) or (obs[new_head_y][new_head_x] > 1):
        global env_state
        env_state = 'closed'

    if env_state == 'open':
        if obs[new_head_y][new_head_x] == -1:
            apple_collected = True
            obs[tail[0]][tail[1]] = if_apple
        obs[new_head_y][new_head_x] = 1

    post_step()

def post_step():
    global env_state
    global score
    global obs
    if env_state == 'closed':
        print(score)
        score = 0
        env_state = 'open'
        obs = reset_env()
        for i in range(1):
            generate_apple()

    if apple_collected is True:
        generate_apple()
        score += 1


# In[4]:





# # RENDERING

# In[5]:
run = True
run = False

def init():
    global score
    global obs
    score = 0
    obs = reset_env()
    generate_apple()


# In[6]:


if renderMode == 0:
    init()

    for i in range(125):
        action = random.choice([-1, 0, 1])
        step(action)
        #
        # if env_state == 'closed':
        #     print(score)
        #     score = 0
        #     env_state = 'open'
        #     world = reset_env()
        #     for i in range(1):
        #         generate_apple()
        #
        # if apple_collected is True:
        #     generate_apple()
        #     score += 1

        plt.ion()
        plt.imshow(obs)
        plt.pause(0.01)
        sleep(0.1)


# In[7]:


# world = reset_env()
# generate_apple()

# step(0)

# plt.ion()
# plt.imshow(world)
# #plt.pause(0.5)


# In[8]:


def hook():
    global extStep
    extStep = random.choice([-1, 0, 1])
    return


# In[9]:


import enum

class logTypes(enum.Enum):
    Info = 0
    Ok = 1
    Warn = 2
    Error = 3

class inputModes(enum.Enum):
    PlayerNative = 0
    PlayerTrans = 1
    PreComputed = 2
    Hook = 3
    PlayerAuto = 4

if renderMode == 1 and run:
    import pygame

    pygame.init()

    # input
    im = inputModes.Hook

    # config
    s    = 80              # cell size in px
    b    = 0               # border size in px
    rl   = True            # render log or not
    rg   = True            # render grid or not
    rs   = True            # render score or not
    fs   = 26              # font size
    fps  = 60              # target frames per second
    clrV = (0, 0, 0)       # void (background)
    clrA = (255, 0, 0)     # apple
    clrH = (0, 255, 0)     # head
    clrB = (0, 255, 0)     # body
    clrF = (255, 255, 255) # foreground
    clrG = (40, 40, 40)    # grid
    queS = 5               # seconds to poll moves when input mode is set to "hook"

    c = 8
    w = c * s
    h = c * s
    oq = s / 4
    oh = s / 2

    global queC

    queF = fps * queS
    queC = 0

    if rl:
        w += s * 8

    ds = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()
    logList = []
    font = pygame.font.Font(pygame.font.get_default_font(), fs)
    maxVal = 0
    stepQ = []

    def getMaxVal():
        m = 0
        for y in obs:
            for x in y:
                if x > m:
                    m = x
        return m

    def getValIndex(val):
        index = 0
        for y in obs:
            for x in y:
                if x == val:
                    return index
                index += 1
        return -1

    def getValPos(val):
        index = getValIndex(val)
        log(index)
        if index == -1:
            return [-1, -1]
        yP = index // c
        xP = index - yP * c
        log("xp: " + str(xP) + " yp:" + str(yP))
        return [xP, yP]

    def orient(xP, yP, val):
        pp = getValPos(val - 1)
        pn = getValPos(val + 1)
        isMax = val == maxVal
        log("jsem blok: " + str(val) + " pp: " + str(pp) + " pn:" + str(pn) + " jsem posledni: " + str(isMax))
        if pp[0] == -1:
            return False
        if pp[0] - 1 == xP and pp[1] == yP:
            if isMax:
                drawTriangle(clrB, (xP + 1) * s, yP * s + oq, (xP + 1) * s, yP * s + oh + oq, xP * s, yP * s + oh)
            else:
                if pn[0] != -1:
                    if pn[1] == yP + 1:
                        drawRect(clrB, xP * s + oq, yP * s + oq, s - oq, oh)
                        drawRect(clrB, xP * s + oq, yP * s + oq + oh, oh, oq)
                        return True
                    elif pn[1] == yP - 1:
                        drawRect(clrB, xP * s + oq, yP * s + oq, s - oq, oh)
                        drawRect(clrB, xP * s + oq, yP * s, oh, oq)
                        return True
                drawRect(clrB, xP * s, yP * s + oq, s, oh)
            return True
        if pp[0] + 1 == xP and pp[1] == yP:
            if isMax:
                drawTriangle(clrB, xP * s, yP * s + oq, xP * s, yP * s + oh + oq, (xP + 1) * s, yP * s + oh)
            else:
                if pn[0] != -1:
                    if pn[1] == yP + 1:
                        drawRect(clrB, xP * s, yP * s + oq, s - oq, oh)
                        drawRect(clrB, xP * s + oq, yP * s + oq + oh, oh, oq)
                        return True
                    elif pn[1] == yP - 1:
                        drawRect(clrB, xP * s, yP * s + oq, s - oq, oh)
                        drawRect(clrB, xP * s + oq, yP * s, oh, oq)
                        return True
                drawRect(clrB, xP * s, yP * s + oq, s, oh)
            return True
        if pp[0]== xP and pp[1] - 1 == yP:
            if isMax:
                drawTriangle(clrB, xP * s + oq, (yP + 1) * s, xP * s + oh + oq, (yP + 1) * s, xP * s + oh, yP * s)
            else:
                if pn[0] != -1:
                    if pn[0] == xP - 1:
                        drawRect(clrB, xP * s + oq, yP * s + oq, oh, s - oq)
                        drawRect(clrB, xP * s, yP * s + oq, oq, oh)
                        return True
                    elif pn[0] == xP + 1:
                        drawRect(clrB, xP * s + oq, yP * s + oq, oh, s - oq)
                        drawRect(clrB, xP * s + oh + oq, yP * s + oq, oq, oh)
                        return True
                drawRect(clrB, xP * s + oq, yP * s, oh, s)
            return True
        if pp[0]== xP and pp[1] + 1 == yP:
            if isMax:
                drawTriangle(clrB, xP * s + oq, yP * s, xP * s + oh + oq, yP * s, xP * s + oh, (yP + 1) * s)
            else:
                if pn[0] != -1:
                    if pn[0] == xP - 1:
                        drawRect(clrB, xP * s + oq, yP * s, oh, s - oq)
                        drawRect(clrB, xP * s, yP * s + oq, oq, oh)
                        return True
                    elif pn[0] == xP + 1:
                        drawRect(clrB, xP * s + oq, yP * s, oh, s - oq)
                        drawRect(clrB, xP * s + oh + oq, yP * s + oq, oq, oh)
                        return True
                drawRect(clrB, xP * s + oq, yP * s, oh, s)
            return True
        return False

    def cell(xP, yP, val):
        if val == 0:
            return
        else:
            clr = clrA
            if val == -1:
                drawCircle(clr, xP * s + oh, yP * s + oh, s)
                return
            if val == 1:
                pn = getValPos(val + 1)
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
                clr = clrH
            elif val >= 2:
                clr = clrB
                t = orient(xP, yP, val)
                if t:
                    return
            drawRect(clr, xP * s, yP * s, s, s)

    def log(text, type = logTypes.Info):
        global logList
        logList.append([str(text), type])

    def drawLine(c, x1, y1, x2, y2, w = 1):
        pygame.draw.line(ds, c, (x1, y1), (x2, y2), w)

    def drawPoly(c, vert):
        pygame.draw.polygon(ds, c, vert)

    def drawQuad(c, x1, y1, x2, y2, x3, y3, x4, y4):
        pygame.draw.polygon(ds, c, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])

    def drawTriangle(c, x1, y1, x2, y2, x3, y3):
        pygame.draw.polygon(ds, c, [(x1, y1), (x2, y2), (x3, y3)])

    def drawRect(c, x, y, w, h):
        pygame.draw.rect(ds, c, pygame.Rect(x, y,  w,  h))

    def drawRectExt(c, x, y, w, h, ow):
        pygame.draw.rect(ds, c, pygame.Rect(x, y,  w,  h), ow)

    def drawText(c, x, y, t):
       ts = font.render(t, True, c)
       ds.blit(ts, (x, y))

    def drawCircle(c, x, y, r):
        pygame.draw.circle(ds, c, (x, y), r / 2)

    def renderLogList():
        if not rl:
            return
        global logList
        index = 0
        for entry in logList:
            c = clrF
            if entry[1] == logTypes.Ok:
                c = (0, 255, 0)
            elif entry[1] == logTypes.Warn:
                c = (255, 165, 0)
            elif entry[1] == logTypes.Error:
                c = (255, 0, 0)
            drawText(c, w / 2 + 10, 10 + index * (fs + 4), entry[0])
            index += 1
        logList = []

    def beforeRender():
        global maxVal
        global extStep

        if extStep != -2:
            stepQ.append(extStep)
            extStep = -2

        maxVal = getMaxVal()

    def clear():
        drawRect(clrV, 0, 0, w, h)

    def renderGrid():
        index = 0
        for _ in obs:
            drawLine(clrG, index * s, 0, index * s, s * c)
            drawLine(clrG, 0, index * s, s * c, index * s)
            index += 1

    def renderScore():
        drawText(clrF, 6, 6, "Skore: " + str(score))

    def input():
        return

    def handleQ():
        global queC
        if queC == 0:
            if len(stepQ) > 0:
                stepI = stepQ.pop()
                log("Proveden pohyb: " + str(stepI), logTypes.Ok)
                step(stepI)
                queC = queF
        else:
            queC -= 1

    def render():

        if im == inputModes.Hook:
            handleQ()

        beforeRender()
        clear()

        if rg:
            renderGrid()

        if rl:
            drawRectExt(clrF, w / 2, 0, w / 2, h, 1)

        xx = 0
        yy = 0
        for y in obs:
            for x in y:
                cell(xx, yy, x)
                xx += 1
            yy += 1
            xx = 0
        renderLogList()

        if rs:
            renderScore()

    if run:
        init()
    while run:
        clock.tick(fps)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                run = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_w:
                    step(0)
                elif e.key == pygame.K_d:
                    step(1)
                elif e.key == pygame.K_a:
                    step(-1)
        hook()
        render()
        pygame.display.update()


# In[9]:





# In[9]:





# In[9]:





# # INPUT

# In[ ]:


## Neural Net and Genetic algorithm
import numpy as np
import tensorflow as tf
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.optimizer_v2.adam import Adam


# In[ ]:


# output layer
actions = [-1, 0, 1]


# In[ ]:


#input layer
input_layer = np.zeros(6)

def preprocess_state(obs): # world and look_dir could be parameters
    # finding look_dir in order to know which objects are on our right etc.
    head = None
    neck = None
    body = None
    tail = None
    tail_value = 0
    for y in range(size):
        for x in range(size):
            if obs[y][x] == 1:
                head = [y, x]
                obs[y][x] += 1
            elif obs[y][x] == 2:
                neck = [y, x]
                obs[y][x] += 1
            elif obs[y][x] > 2:
                body = [y, x]
                obs[y][x] += 1
            if obs[y][x] > tail_value:
                tail = [y, x]
                tail_value = obs[y][x]

    y = head[0]-neck[0]
    x = head[1]-neck[1]
    look_dir = [y, x]

    look_dirs = [[0, -1], [-1, 0], [0, 1], [1, 0]]
    look_dir_index = look_dirs.index(look_dir)
    info_left = []
    indices_left = [] #actually its positions
    info_straight = []
    indices_straight = []
    info_right = []
    indices_right = []


    for ii in range(1, 4):
        shift_left = look_dirs[look_dir_index-1]
        pixel_left_y = head[0]+ii*(shift_left[0])
        pixel_left_x = head[1]+ii*(shift_left[1])
        if (pixel_left_x > size-1) or (pixel_left_y > size-1) or (pixel_left_x < 0) or (pixel_left_y < 0):      #if we can still move
            info_left.append(-2)
            indices_left.append(ii)
            break
        if obs[pixel_left_y][pixel_left_x] != 0:
            info_left.append(obs[pixel_left_y][pixel_left_x])
            indices_left.append(ii)

    for ii in range(1, 4):
        shift_straight = look_dirs[look_dir_index]
        pixel_straight_y = head[0]+ii*(shift_straight[0])
        pixel_straight_x = head[1]+ii*(shift_straight[1])
        if (pixel_straight_x > size-1) or (pixel_straight_y > size-1) or (pixel_straight_x < 0) or (pixel_straight_y < 0):      #if we can still move
            info_straight.append(-2)
            indices_straight.append(ii)
            break
        if obs[pixel_straight_y][pixel_straight_x] != 0:
            info_straight.append(obs[pixel_straight_y][pixel_straight_x])
            indices_straight.append(ii)

    for ii in range(1, 4):
        if look_dir_index == 3:
            shift_right = look_dirs[0]
        else:
            shift_right = look_dirs[look_dir_index+1]
        pixel_right_y = head[0]+ii*(shift_right[0])
        pixel_right_x = head[1]+ii*(shift_right[1])
        if (pixel_right_x > size-1) or (pixel_right_y > size-1) or (pixel_right_x < 0) or (pixel_right_y < 0):      #if we can still move
            info_right.append(-2)
            indices_right.append(ii)
            break
        if obs[pixel_right_y][pixel_right_x] != 0:
            info_right.append(obs[pixel_right_y][pixel_right_x])
            indices_right.append(ii)

    if len(indices_left) != 0:
        input_layer[0] = 1 if ((indices_left[0] == 1) and ((info_left[0] > 1 and info_left[0] != tail_value) or info_left[0] == -2)) else 0 # there is an obsticle on the left (distance 1)
    if len(indices_straight) != 0:
        input_layer[1] = 1 if ((indices_straight[0] == 1) and ((info_straight[0] > 1 and info_straight[0] != tail_value) or info_straight[0] == -2)) else 0
    if len(indices_right) != 0:
        input_layer[2] = 1 if ((indices_right[0] == 1) and ((info_right[0] > 1 and info_right[0] != tail_value) or info_right[0] == -2)) else 0
    input_layer[3] = 1 if (-1 in info_left) else 0 # food in range 3 to the right
    input_layer[4] = 1 if (-1 in info_straight) else 0
    input_layer[5] = 1 if (-1 in info_right) else 0

    return input_layer


# In[ ]:


def onehot_encode(index, length):
    a = np.zeros((length,), dtype=np.uint8)
    a[index] = 1
    return a


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


import sys
import numpy as  np
import matplotlib



# In[ ]:


# 1 neuron:
# inputs = [1, 2, 3]
# weights = [0.2, 0.8, -0.5]
# bias = 2
# output = inputs[0]*weights[0] + inputs[1]*weights[1] + inputs[2]*weights[2] + bias


# In[ ]:





# In[ ]:


# inputs = [1, 2, 3, 2.5]
# weights = [[0.2, 0.8, -0.5, 1],
#  [0.5, -0.91, 0.26, -0.5],
#  [-0.26, -0.27, 0.17, 0.87]]
# biases = [2, 3, 0.5]
# # Output of current layer
# layer_outputs = []
# # For each neuron
# for neuron_weights, neuron_bias in zip(weights, biases):
#  # Zeroed output of given neuron
#  neuron_output = 0
#  # For each input and weight to the neuron
#  for n_input, weight in zip(inputs, neuron_weights):
#  # Multiply this input by associated weight
#  # and add to the neuron's output variable
#  neuron_output += n_input*weight
#  # Add bias
#  neuron_output += neuron_bias
#  # Put neuron's result to the layer's output list
#  layer_outputs.append(neuron_output)
# print(layer_outputs)


# In[ ]:





# In[ ]:


# #batch, 1 layer
#
# import numpy as np
# inputs = [[1.0, 2.0, 3.0, 2.5],
#  [2.0, 5.0, -1.0, 2.0],
#  [-1.5, 2.7, 3.3, -0.8]]
# weights = [[0.2, 0.8, -0.5, 1.0],
#  [0.5, -0.91, 0.26, -0.5],
#  [-0.26, -0.27, 0.17, 0.87]]
# biases = [2.0, 3.0, 0.5]
# layer_outputs = np.dot(inputs, np.array(weights).T) + biases
# print(layer_outputs)
# >>>
# array([[ 4.8 1.21 2.385],
#  [ 8.9 -1.81 0.2 ],
#  [ 1.41 1.051 0.026]])


# In[ ]:


# np.random.seed(0)

# X = [[1, 2, 3, 2.5, 1, 2],
#      [2.0, 5.0, -1.0, 2.0, 1, 2],
#      [-1.5, 2.7, 3.3, -0.8, 1, 2]]

X = preprocess_state(obs)

# Dense layer
class Layer_Dense:
 # Layer initialization
    def __init__(self, n_inputs, n_neurons):
        # Initialize weights and biases
        self.weights = 0.10 * np.random.randn(n_inputs, n_neurons) #already transposed matrix of weights for every neuron
        self.biases = np.zeros((1, n_neurons))
    # Forward pass
    def forward(self, inputs):
    # Calculate output values from inputs, weights and biases
        self.output = np.dot(inputs, self.weights) + self.biases

# ReLU activation
class Activation_ReLU:
     # Forward pass
     def forward(self, inputs):
         # Calculate output values from input
         self.output = np.maximum(0, inputs)

dense1 = Layer_Dense(6, 5)

activation1 = Activation_ReLU()
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


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




