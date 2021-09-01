import pygame as pg
import numpy as np
from Pkg.Denovo_Learning.Parameters import  Parameters
from pygame.rect import *


class Cursor:

    def __init__(self):
        self.curr_x = int( Parameters.width / 2 )
        self.curr_y = int( Parameters.height / 2 )
        self.max_x = Parameters.width - Parameters.cursor_diameter
        self.max_y = Parameters.height - Parameters.cursor_diameter

    def update(self, Screen):
        pg.draw.ellipse(Screen.screen, Parameters.gray,
                        Rect(self.curr_x, self.curr_y, Parameters.cursor_diameter, Parameters.cursor_diameter), width = 1)

    def mode(self, mode, a, b):
        if mode == 'base':

            prev_x = a * 2
            prev_y = b * 2

            self.curr_x += prev_x
            self.curr_y += prev_y

            if self.curr_y <= 0:
                self.curr_y = 0
            elif self.curr_y >= self.max_y:
                self.curr_y = self.max_y

            if self.curr_x <= 0:
                self.curr_x = 0
            elif self.curr_x >= self.max_x:
                self.curr_x = self.max_x

            return [int(self.curr_x), int(self.curr_y)]

        if mode == 'adapt':

            self.degree = -90

            prev_x = a * 2
            prev_y = b * 2

            if prev_x > 0:
                theta_final = self.degree + np.rad2deg(np.arctan(prev_y / prev_x))
            elif prev_x < 0:
                theta_final = 180 + self.degree + np.rad2deg(np.arctan(prev_y / prev_x))

            prev_x_rot = np.sqrt(prev_x ** 2 + prev_y ** 2) * np.cos(np.deg2rad(theta_final))
            prev_y_rot = np.sqrt(prev_x ** 2 + prev_y ** 2) * np.sin(np.deg2rad(theta_final))

            self.curr_x += prev_x_rot
            self.curr_y += prev_y_rot

            if self.curr_y <= 0:
                self.curr_y = 0
            elif self.curr_y >= self.max_y:
                self.curr_y = self.max_y

            if self.curr_x <= 0:
                self.curr_x = 0
            elif self.curr_x >= self.max_x:
                self.curr_x = self.max_x

            return [self.curr_x, self.curr_y]

        if mode == 'reverse':
            self.degree = 0

            prev_x = a * 3
            prev_y = b * 3

            self.curr_x -= prev_y
            self.curr_y -= prev_x

            if self.curr_y <= 0:
                self.curr_y = 0
            elif self.curr_y >= self.max_y:
                self.curr_y = self.max_y

            if self.curr_x <= 0:
                self.curr_x = 0
            elif self.curr_x >= self.max_x:
                self.curr_x = self.max_x

            return [self.curr_x, self.curr_y]
