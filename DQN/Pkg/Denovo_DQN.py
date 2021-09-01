import gym
import numpy as np
import pygame as pg
import time
import PIL.Image as pilimg

from Pkg.Denovo_Learning.Parameters import Parameters
from Pkg.Denovo_Learning.Screen import Screen
from Pkg.Denovo_Learning.Target import Target
from Pkg.Denovo_Learning.Event import Event
from Pkg.Denovo_Learning.Cursor import Cursor


class Denovo_Env(gym.Env):

    def __init__(self):

        # Get the parameters // Pkg.Denovo_Learning.Parameters.py

        Parameters()

        self.clock = pg.time.Clock()
        self.screen = Screen()
        self.target = Target()
        self.cursor = Cursor()
        self.event = Event()
        pg.mouse.set_visible(False)

        # Action_space // r = 5 , theta : 45 * Diescrete(8)

        self.action_space = gym.spaces.Discrete(9) # range(0,8) not include 8

        self.state = [int( Parameters.width / 2 ), int( Parameters.height / 2 ), self.target.get_pos()[0], self.target.get_pos()[1]]

        self.start = time.time()
        self.count = 0

    def reset(self):
        Parameters()

        self.count = 0
        self.done = False
        self.start = time.time()

        self.screen = Screen()
        self.target = Target()
        self.cursor = Cursor()
        self.event = Event()

        self.state = [int( Parameters.width / 2 ), int( Parameters.height / 2 ), self.target.get_pos()[0], self.target.get_pos()[1]]

        return self.state

    def step(self, action):

        # observation

        if action != 8:
            self.action = [2, action * 45]
        else:
            self.action = [0, 0]

        self.target.move()
        self.state[0], self.state[1] = self.cursor.mode('base',
                                      self.action[0] * np.cos(np.deg2rad(self.action[1])),
                                      self.action[0] * np.sin(np.deg2rad(self.action[1])))

        self.state = [self.state[0], self.state[1], self.target.get_pos()[0], self.target.get_pos()[1]]

        # done

        self.done = False
        self.count += 1

        # reward

        if self.state[0] >= self.state[2] and self.state[0] <= self.state[2] + Parameters.target_diameter\
        and self.state[1] >= self.state[3] and self.state[1] <= self.state[3] + Parameters.target_diameter:
            reward = 20

        else:
            reward = (1 / round((np.sqrt((self.state[0]-self.state[2]) ** 2 + (self.state[1] - self.state[3]) ** 2) / 100), 3))
            if reward > 19:
                reward = 19
            reward /= 10

        self.time_limit = 30

        if round((np.sqrt((self.state[0]-self.state[2]) ** 2 + (self.state[1] - self.state[3]) ** 2) / 100), 3) > 10:
            self.done = True

        if self.count > self.time_limit * Parameters.hertz:
            self.done = True


        # Info

        info = {}

        return self.state, reward, self.done, info

    def render(self):

        pg.event.pump()

        self.clock.tick(Parameters.hertz)
        self.screen.overwrite()
        self.target.update('base', self.screen)
        self.cursor.update(self.screen)

        if self.state[0] >= self.state[2] and self.state[0] <= self.state[2] + Parameters.target_diameter \
                and self.state[1] >= self.state[3] and self.state[1] <= self.state[3] + Parameters.target_diameter:
            self.event.hit_target(self.screen, self.target)

        self.screen.flip()

        pg.image.save(self.screen.screen, '/Users/imlim/Downloads/Git/Python/Denovo/DQN/a.bmp')

        return np.array(pilimg.open('/Users/imlim/Downloads/Git/Python/Denovo/DQN/a.bmp'))[:,:,:3]

