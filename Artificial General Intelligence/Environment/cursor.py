###########################################################################
## Lubrary import 
###########################################################################
import pygame as G
import numpy as np
from parameters import Parameters
from pygame.rect import *

###########################################################################
## Class Definition
###########################################################################
class Cursor:
    '''
    게임의 커서를 정의하기 위한 클래스
    
    Attributes:
        _param : 파라미터 클래스를 호출
               : class object
               
        cur_x : time step t의 커서 x postion // 초기 값은 960
              : number
              
        cur_y : time step t의 커서 y postion // 초기 값은 540
              : number
              
        max_x : 커서가 가질 수 있는 x 최댓값
              : number
              
        max_y : 커서가 가질 수 있는 y 최댓값
              : number
              
        cur_color : 커서의 색상
              : G.color() object
    
    Methods:
        update : 커서를 스크린에 출력하기 위한 메소드
               : (+) 모양으로 모양을 정의하였다. 두께는 3 pixel이고, 길이는 20 pixel이다.
               : +35를 기준으로 하였고, 이는 타겟의 정중앙을 의미하기 위함이다.
               
            Args:
                screen : 커서를 디스플레이 할 스크린
                       : class object
                   
        move : 커서의 좌표를 이동시키기 위한 메소드
             
            Args:
                mode : 현재 게임의 mode
                     : str
                     
                action : 조이스틱을 움직인 정도를 나타내는 x, y
                       : numpy array
                       
            Return:
                [int(self.cur_x), int(self.cur_y)] : 이동 된 커서의 좌표.
                                                   : list(int, int)
    '''
    
    def __init__(self):
        self._param = Parameters()
        self.cur_x = self._param.init_x
        self.cur_y = self._param.init_y
        self.max_x = self._param.width - self._param.target_diameter
        self.max_y = self._param.height - self._param.target_diameter
        self.cur_color = self._param.white
        
    def update(self, screen):
        G.draw.line(screen.screen, self.cur_color, (self.cur_x + 25, self.cur_y + 35), (self.cur_x + 45, self.cur_y + 35), 3)
        G.draw.line(screen.screen, self.cur_color, (self.cur_x + 35, self.cur_y + 25), (self.cur_x + 35, self.cur_y + 45), 3)
        
    def move(self, mode, action):
        act_x = action[0] * np.cos(np.deg2rad(action[1]))
        act_y = action[0] * np.sin(np.deg2rad(action[1]))
        
        if mode == 'base':
            self.cur_x, self.cur_y = base(self.cur_x, self.cur_y, act_x, act_y, self.max_x, self.max_y)
        elif mode == 'adapt':
            self.cur_x, self.cur_y = adapt(self.cur_x, self.cur_y, act_x, act_y, self.max_x, self.max_y)
        elif mode == 'reverse':
            self.cur_x, self.cur_y = reverse(self.cur_x, self.cur_y, act_x, act_y, self.max_x, self.max_y)
        else:
            print('Choos the mode among...')
            RuntimeError()
            
        return [int(self.cur_x), int(self.cur_y)]
    

###########################################################################
## Mode Definition
###########################################################################
def base(cur_x, cur_y, act_x, act_y, max_x, max_y):
    '''
    조이스틱 모드를 'base'로 설정하는 함수.
    'base' 모드는 조이스틱이 기존에 생각하던 방향과 동일하게 움직인다.
    
    커서의 x, y 좌표에 조이스틱에서 받은 x, y 좌표를 더하여 커서의 좌표를 업데이트한다.
    
    Args:
        cur_x : time step t의 커서 x postion
              : number
              
        cur_y : time step t의 커서 y postion
              : number
              
        act_x : time step t의 조이스틱 x postion
              : number
              
        act_y : time step t의 조이스틱 y postion
              : number
              
        max_x : 커서가 가질 수 있는 x 최댓값
              : number
              
        max_y : 커서가 가질 수 있는 y 최댓값
              : number
              
    Returns:
        cur_x, cur_y : time step (t+1)의 커서 x, y position
                     : tuple(float, float)
    '''
    
    cur_x += act_x
    cur_y += act_y
    
    if cur_y <= 0:
        cur_y = 0
    elif cur_y >= max_y:
        cur_y = max_y
        
    if cur_x <= 0:
        cur_x = 0
    elif cur_x >= max_x:
        cur_x = max_x
    
    return cur_x, cur_y

def adapt(cur_x, cur_y, act_x, act_y, max_x, max_y, degree = -90):
    '''
    조이스틱 모드를 'adapt'로 설정하는 함수.
    'adapt' 모드는 조이스틱이 기존에 생각하던 방향에서 90도 회전한 방향으로 움직인다.
    
    커서의 x, y 좌표에 조이스틱에서 받은 x, y 좌표를 90도 회전 후 더하여 커서의 좌표를 업데이트한다.
    
    Args:
        cur_x : time step t의 커서 x postion
              : number
              
        cur_y : time step t의 커서 y postion
              : number
              
        act_x : time step t의 조이스틱 x postion
              : number
              
        act_y : time step t의 조이스틱 y postion
              : number
              
        max_x : 커서가 가질 수 있는 x 최댓값
              : number
              
        max_y : 커서가 가질 수 있는 y 최댓값
              : number
    
    Returns:
        cur_x, cur_y : time step (t+1)의 커서 x, y position
                     : tuple(float, float)
    '''
    
    prev_x = act_x
    prev_y = act_y
    
    if prev_x >= 0:
        theta_final = degree + np.rad2deg(np.arctan(prev_y / prev_x))
    elif prev_x < 0:
        theta_final = 180 + dgree + np.rad2deg(np.arctan(prev_y / prev_x))
    
    prev_x_rot = np.sqrt(prev_x ** 2 + prev_y ** 2) * np.cos(np.deg2rad(theta_final))
    prev_y_rot = np.sqrt(prev_x ** 2 + prev_y ** 2) * np.sin(np.deg2rad(theta_final))
                                                             
    cur_x += prev_x_rot
    cur_y += prev_y_rot
    
    if cur_y <= 0:
        cur_y = 0
    elif cur_y >= max_y:
        cur_y = max_y
        
    if cur_x <= 0:
        cur_x = 0
    elif cur_x >= max_x:
        cur_x = max_x
    
    return cur_x, cur_y

def reverse(cur_x, cur_y, act_x, act_y, max_x, max_y):
    '''
    조이스틱 모드를 'reverse'로 설정하는 함수.
    'reverse' 모드는 조이스틱이 기존에 생각하던 방향에 45도를 기준으로 반전된 방향으로 움직인다.
    
    커서의 x, y 좌표에 조이스틱에서 받은 x, y 좌표를 더하여 커서의 좌표를 업데이트한다.
    
    Args:
        cur_x : time step t의 커서 x postion
              : number
              
        cur_y : time step t의 커서 y postion
              : number
              
        act_x : time step t의 조이스틱 x postion
              : number
              
        act_y : time step t의 조이스틱 y postion
              : number
              
        max_x : 커서가 가질 수 있는 x 최댓값
              : number
              
        max_y : 커서가 가질 수 있는 y 최댓값
              : number
    
    Returns:
        cur_x, cur_y : time step (t+1)의 커서 x, y position
                     : tuple(float, float)
    '''
    
    prev_x = act_x
    prev_y = act_y
    
    cur_x -= prev_y
    cur_y -= prev_x
    
    if cur_y <= 0:
        cur_y = 0
    elif cur_y >= max_y:
        cur_y = max_y
        
    if cur_x <= 0:
        cur_x = 0
    elif cur_x >= max_x:
        cur_x = max_x
    
    return cur_x, cur_y