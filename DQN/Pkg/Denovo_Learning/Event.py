from Pkg.Denovo_Learning.Parameters import Parameters
import pygame as pg

class Event:

    def __init__(self):
        pass

    def hit_target(self,Screen, Target):
        pg.draw.ellipse(Screen.screen, Parameters.red, Target.rect, width = 0)
