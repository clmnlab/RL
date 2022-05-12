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
def makedir(dir_path, name):
    '''
    강화학습 모델을 저장 할 폴더를 생성 및 위치 지정을 위한 함수
    
    Args:
        dir_path : 모델을 저장 할 상위 폴더 ( 절대 위치를 권장 )
                 : str
                 
        name : 모델을 저장 할 폴더이름
             : str
    Return:
        directory : 디렉토리 절대 위치를 반환
                  : str
    '''
    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    if '/' in dir_path[-1]:
        pass
    else:
        dir_path = dir_path + '/'
    
    directory = dir_path + name
    
    if not os.path.exists(directory):
        os.makedirs(directory)
        os.makedirs(directory + '/Actor')
        os.makedirs(directory + '/Critic')
    
    print('=' * 50)
    print('Directory has been made...')
    print('Directory path : {}'.format(directory))
    print('=' * 50)
    
    return directory
