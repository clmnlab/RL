from pygame.rect import *
from Pkg.Denovo_Learning.Parameters import Parameters

import pygame as pg

class Target:

    def __init__(self):
        self.rect = Rect(Parameters.target_x, Parameters.target_y, Parameters.target_diameter, Parameters.target_diameter)

    def move(self):
        self.rect.move_ip(Parameters.speed)

        if self.rect.left < 0:
            Parameters.speed[0] *= -1
        if self.rect.right > Parameters.width:
            Parameters.speed[0] *= -1
        if self.rect.top < 0:
            Parameters.speed[1] *= -1
        if self.rect.bottom > Parameters.height:
            Parameters.speed[1] *= -1




    def update(self, mode, Screen):
        if mode == 'base':
            self.target = pg.draw.ellipse(Screen.screen, Parameters.gray, self.rect, width = 1)
        elif mode == 'adapt':
            self.target = pg.draw.ellipse(Screen.screen, Parameters.blue, self.rect, width = 1)
        elif mode == 'reverse':
            self.target = pg.draw.ellipse(Screen.screen, Parameters.yellow, self.rect, width = 1)

    def get_pos(self):
        return [list(self.rect.copy())[0],list(self.rect.copy())[1]]
