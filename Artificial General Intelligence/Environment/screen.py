###########################################################################
## Lubrary import 
###########################################################################
import pygame as G
from parameters import Parameters

###########################################################################
## Class Definition
###########################################################################
class Screen:
    '''
    게임에 사용 될 스크린을 정의하기 위한 클래스
    
    Attributes:
        _param : 파라미터 클래스를 호출
        screen : 스크린 정의
        
    Methods:
        overwrite : 화면을 검은색으로 덮어씌움으로써 오브젝트들을 화면에서 지움.
        flip : 스크린을 컴퓨터 화면에 보여줌.
        
    '''
    
    def __init__(self):
        G.init()
        self._param = Parameters()
        self.screen = G.display.set_mode([self._param.width, self._param.height], flags=G.HIDDEN)
        
    def overwrite(self):
        self.screen.fill(self._param.black)
        
    def flip(self):
        G.display.flip()