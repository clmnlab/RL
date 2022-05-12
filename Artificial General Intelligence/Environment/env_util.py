###########################################################################
## Lubrary import 
###########################################################################
import os
import pygame as G
import numpy as np
import matplotlib.pyplot as plt

###########################################################################
## Function Definition
###########################################################################
def os_driver(tmp=False):
    '''
    서버에서 강화학습을 시킬 시 video와 audio driver를 off 시키기 위한 함수.
    
    Args:
        tmp : Video / Audio driver를 on / off 하는 트리거
            : Boolean ( True : video와 audio driver "ON" // False : video와 audio driver "OFF" ) 
    '''
    
    if tmp == False:
        os.environ["SDL_VIDEODRIVER"] = 'dummy'
        os.environ["SDL_VIDEODRIVER"] = 'dummy'
    else:
        pass

def visible_mouse(tmp=True):
    '''
    화면에서 마우스를 표기 여부를 결정하기 위한 함수
    
    Args:
        tmp : 마우스 표기를 on / off 하는 트리거
            : Boolean ( True : mouse "ON" // False : mouse "OFF" ) 
    '''
    
    G.mouse.set_visible(tmp)
    
def clock_tick(time):
    '''
    게임의 화면 전환 hertz를 설정하기 위한 함수
    하지만, 하드웨어의 스펙상 조금씩 다를 수 있다.
    
    Args:
        time : Hertz ( i.e. 60이라면 1초에 60번의 화면전환 )
             : int
    '''
    
    clock = G.time.Clock()
    clock.tick(time)
    
def plot_image(frame):
    '''
    프레임을 그리기 위한 함수
    
    Args:
        frame : 강화학습이 실제 입력으로 사용하는 프레임 
              : numpy array
    '''
    frame = frame.reshape(1, 84, 84).transpose((2, 1, 0))
    plt.imshow(frame, cmap='gray')
    plt.show()