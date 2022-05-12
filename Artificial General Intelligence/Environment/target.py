###########################################################################
## Lubrary import 
###########################################################################
import pygame as G

from pygame.rect import *
from parameters import Parameters

###########################################################################
## Class Definition
###########################################################################
class Target:
    '''
    게임의 타겟을 정의하기 위한 클래스
    타겟은 경로가 정해져있다.
    
    Attributes:
        _param : 파라미터 클래스를 호출
        rect : 타겟에 대한 정보를 정의.
        target : rect를 circle으로 만든 최종 타겟
        idx : 타겟 경로의 인덱스
    
    Methods:
        move : 타겟의 좌표를 이동시키기 위한 메소드
            
            Args:
                path : 정해진 경로 
                     : numpy array
                     
                idx : 경로의 인덱스
                    : int
                    
        update : 커서를 스크린에 출력하기 위한 메소드
            
            Args:
                mode : 현재 게임의 모드
                     : str
                     
                screen : 타겟을 디스플레이 할 스크린
                       : class object
                       
        pos : 타겟의 좌표를 반환하기 위한 메소드
            
            Return:
                [list(self.rect.copy())[0], list(self.rect.copy())[1]] : 타겟의 좌표를 반환
                                                                       : list(int,int)
    '''
    
    def __init__(self):
        self._param = Parameters()
        self.rect = Rect(self._param.init_x, self._param.init_y, self._param.target_diameter, self._param.target_diameter)
        self.target = None
        self.idx = 0
        
    def move(self, path, idx):
        self.rect = Rect(path[idx][0], path[idx][1], self._param.target_diameter, self._param.target_diameter)
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self._param.width:
            self.rect.right = self._param.width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self._param.height:
            self.rect.bottom = self._param.height
    
    def update(self, mode, screen):
        if mode == 'base':
            self.target = G.draw.ellipse(screen.screen, self._param.gray, self.rect, 0)
        elif mode == 'adapt':
            self.target = G.draw.ellipse(screen.screen, self._param.blue, self.rect, 0)
        elif mode == 'reverse':
            self.target = G.draw.ellipse(screen.screen, self._param.yellow, self.rect, 0)
            
    def pos(self):
        return [list(self.rect.copy())[0], list(self.rect.copy())[1]]