###########################################################################
## Library import 
###########################################################################
import pygame as G

###########################################################################
## Class Definition
###########################################################################
class Parameters:
    '''
    게임에 사용 될 파라미터들을 정의하기 위한 클래스
    
    Attributes:
        Color : 게임 내 사용 될 색상 파라미터. ( e.g. red, gray, etc. )
        Length : 게임 내 사용 될 디스플레이 및 오브젝트의 길이 파라미터. ( e.g. width, cursor_diameter, target_diameter )
        Duration : 시간 및 반복 횟수 파라미터. ( e.g. hertz, time, etc. )
        Position : 초기 타겟과 커서의 위치 파라미터. ( e.g. init_x, init_y )
    '''
    
    def __init__(self):
        ###########################################################################
        ## Color
        ###########################################################################
        self.red = G.Color(255, 0, 0)
        self.gray = G.Color(128, 128, 128)
        self.green = G.Color(0, 255, 0)
        self.white = G.Color(255, 255, 255)
        self.black = G.Color(0, 0, 0)
        self.blue = G.Color(0, 0, 255)
        self.yellow = G.Color(255, 255, 0)
        
        ###########################################################################
        ## Length
        ###########################################################################
        self.width = 1920
        self.height = 1080
        self.cursor_diameter = 20
        self.target_diameter = 70
        
        ###########################################################################
        ## Duration
        ###########################################################################
        self.hertz = 60
        self.time = 25
        self.trial = 20
        self.duration = self.hertz * self.time * self.trial
        self.count = 0
        self.index = 0
        
        ###########################################################################
        ## Position
        ###########################################################################
        self.init_x = 960
        self.init_y = 540
        