import pygame as pg
from Pkg.Denovo_Learning.Parameters import Parameters

class Screen:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode([Parameters.width, Parameters.height])

    def overwrite(self):
        self.screen.fill(Parameters.black)

    def flip(self):
        pg.display.flip()