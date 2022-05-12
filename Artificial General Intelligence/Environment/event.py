###########################################################################
## Library import 
###########################################################################
import pygame as G
from parameters import Parameters

###########################################################################
## Class Definition
###########################################################################
class Event:
    '''
    게임의 이벤트를 정의하기 위한 클래스
    
    Attributes:
        _param : 파라미터 클래스를 호출
        event_color : 이벤트 트리거시 타겟의 색상
        
    Methods:
        hit_target : 커서가 타겟 범위 내에 위치하면 실행되는 메소드
                   
            Args:
                screen : 이벤트를 디스플레이 할 스크린
                       : class object
                       
                target : 타겟 정보를 얻기 위해 타겟 호출
                       : class object
    '''
    
    def __init__(self):
        self._param = Parameters()
        self.event_color = self._param.red
    
    def hit_target(self, screen, target):
        G.draw.ellipse(screen.screen, self.event_color, target.rect, 0)
     
