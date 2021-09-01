import pygame as pg

class Parameters:

    def __init__(self):
        Parameters.color(self)
        Parameters.display(self)
        Parameters.time(self)
        Parameters.control(self)

    def color(self):
        Parameters.red = pg.Color(255, 0, 0)
        Parameters.gray = pg.Color(128, 128, 128)
        Parameters.green = pg.Color(0, 255, 0)
        Parameters.white = pg.Color(255, 255, 255)
        Parameters.black = pg.Color(0, 0, 0)
        Parameters.blue = pg.Color(0, 0, 255)
        Parameters.yellow = pg.Color(255,255,0)


    def display(self):
        Parameters.width = 1440
        Parameters.height = 850
        Parameters.cursor_diameter = 20
        Parameters.target_diameter = 70

    def time(self):
        Parameters.hertz = 30
        Parameters.time_1 = 24
        Parameters.duration = Parameters.hertz * Parameters.time_1

    def control(self):
        Parameters.count = 0
        Parameters.index = 0
        Parameters.run = True
        Parameters.speed = [2, 2]
        Parameters.target_x = 500
        Parameters.target_y = 500
