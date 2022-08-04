import random
import gym
import gym_snake
import numpy as np

env = gym.make("Snake-8x8-4a-v0")
obs = env.reset()

for i in  range(1000):
    print(i)
    env.render()

    action = random.choice([0, 1, 2])
    obs, reward, done = env.step(action)

    if done:
        obs, env.reset()

env.close()