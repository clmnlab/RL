###########################################################################
## Library import 
###########################################################################
import os, sys, gym, cv2, time
import numpy as np
import pygame as G
import matplotlib.pyplot as plt

sys.path.append('/home/lim/Artificial General Intelligence/Environment')

from parameters import Parameters
from screen import Screen
from target import Target
from event import Event
from cursor import Cursor
from env_util import *

########################################################################################
## Path Definition  : 실제 스크린은 int값으로 디스플레이하기 때문에 데이터 타입을 int로 변환
########################################################################################
# path = np.load('/home/lim/Artificial General Intelligence/Data/total_path.npy').astype('int')

os_driver(False)

########################################################################################
## Class Definition
########################################################################################
class RL_game(gym.Env):
    '''
    강화학습과 상호작용 할 게임 클래스
    
    Attributes:
        parameter : 파라미터 클래스
                  : class object
                  
        clock : 클럭 클래스
              : class object
                  
        screen : 스크린 클래스
               : class object
                  
        target : 타겟 클래스
               : class object
                  
        cursor : 커서 클래스
               : class object
                  
        event : 이벤트 클래스
              : class object
                  
        done : reset을 위해 사용.
             : Boolean ( True : Reset 함수를 호출 / False : 현재 환경을 유지 )
        
        count : 타겟 경로의 인덱스를 지정.
              : int
              
        mode : 조이스틱 모드를 지정
             : str
             
    Methods:
        step : 강화학습 알고리즘으로부터 action을 받아 cursor의 위치를 업데이트 시킴.
             : 호출 될 때마다 count를 증가시킴으로써 타겟의 위치를 업데이트 시킴.
             : done이 False가 되면 step함수는 초기화된다.
             :  1. 타겟과 커서간의 거리가 350 pixel 이상일 때
             :  2. count가 duration과 같아질 때
             
             Args:
                 r, theta : 강화학습으로부터 얻은 r, theta
                          : int
                          
                 path : 이미 저장된 경로파일
                      : numpy array
                 
             Return:
                 state : 강화학습으로부터 얻은 행동으로 업데이트 시킨 커서와 time step에 따른 타겟의 위치
                       : numpy array
                       
                 reward : 타겟과 커서간의 거리에 대한 Inverse Gaussian
                        : float
                        
                 done : 현재 step을 멈추고 게임을 다시 시작할 것인지 아닌지 결정
                      : Boolean ( True : Reset 함수를 호출 / False : 현재 환경을 유지 )
                      
                 info : 게임의 정보이지만 딱히 넣을 것이 없어서 비워둠
                      : dict
        
        reset : 게임을 초기화 시킴.
              :  1. count 변수 0으로 초기화
              :  2. done 변수를 Fasle로 초기화
              :  3. 타겟과 커서 클래스 초기화
              :  4. 이벤트 클래스 초기화
        
        render : 스크린에 타겟과 커서를 디스플레이시킴.
               :  1. 화면을 검은색으로 채움
               :  2. 타겟을 그림
               :  3. 만약 타겟 내 커서가 있으면 빨간색으로 타겟을 그림
               :  4. 커서를 그림
        
        to_frame : input으로 사용 할 이미지 생성.
        
            Args:
                width : input으로 사용 할 이미지의 width
                      : int
                height : input으로 사용 할 이미지의 height
                       : int
            
            Return : image
                   : numpy array
                
    '''
    def __init__(self, mode):
        
        self.parameter = Parameters()
        self.clock = G.time.Clock()
        self.screen = Screen()
        self.target = Target()
        self.cursor = Cursor()
        self.event = Event()
        visible_mouse(False)
        
        self.done = False
        self.count = 0
        self.mode = mode
        
        # Action
        act_high = 1.0
        self.action_r = gym.spaces.Box(low=np.float(0), high=np.float(act_high), shape=(1,))
        self.action_theta = gym.spaces.Box(low=np.float(-act_high), high=np.float(act_high), shape=(1,))
        
    def step(self, r, theta, path):
        self.target.move(path, idx=self.count)
        self.action = np.array([r[0] * 6, theta[0] * 180])
        
        cursor_state = self.cursor.move(self.mode, self.action)
        
        self.state = np.array([cursor_state[0], cursor_state[1], self.target.pos()[0], self.target.pos()[1]], dtype=np.float)
        
        distance = euclidean_distance(self.state)
        reward = distance_reward(distance, 100)
        
        info = {}
        
        if distance >= 350:
            self.done = True
        
        self.count += 1
        
        if self.count != 0 and self.count % 1500 == 0:
            self.cursor = Cursor()
        if self.count == self.parameter.duration:
            self.done = True
        
        return self.state, reward, self.done, info
    
    def reset(self):
        self.count = 0
        self.done = False
        self.target = Target()
        self.cursor = Cursor()
        self.event = Event()
        
        self.state = np.array([self.parameter.init_x, self.parameter.init_y, self.parameter.init_x, self.parameter.init_y], dtype=np.float)
        
        return self.state
    
    def render(self):
        G.event.pump()
        clock_tick(self.parameter.hertz)
        self.screen.overwrite()
        self.target.update(self.mode, self.screen)
        
        if hit(self.state, self.parameter):
            self.event.hit_target(self.screen, self.target)
        else:
            pass
        
        self.cursor.update(self.screen)
        self.screen.flip()
    
    def to_frame(self, width, height):
        self.render()
        
        string_image = G.image.tostring(self.screen.screen, 'RGB')
        tmp_surf = G.image.fromstring(string_image, (self.parameter.width, self.parameter.height), 'RGB')
        tmp = G.surfarray.array3d(tmp_surf)
        tmp = tmp.transpose((1, 0, 2))
        
        img_pad = np.pad(tmp, ((448, 448), (448,448), (0, 0)))
        crop_img = img_pad[int(self.state[3]) : int(self.state[3]) + 896, int(self.state[2]) : int(self.state[2]) + 896, :]
        image = cv2.resize(crop_img, [width, height], interpolation=cv2.INTER_AREA)
        
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        return image
        
###########################################################################
## Function Definition
###########################################################################
def plot_image(frame, width, height):
    '''
    실제 강화학습에 들어 갈 input 이미지를 시각화하기 위함.
    
    Args:
        frame : 실제 강화학습에 들어가는 input 데이터
              : numpy array
        
        width : 시각화 될 이미지의 width
              : int
        
        height : 시각화 될 이미지의 height
               : int
    '''
    
    frame = frame.reshape(1, width, height).transpose(1, 2, 0)
    plt.imshow(frame, cmap = 'gray')
    plt.show()
    
def euclidean_distance(state):
    '''
    타겟과 커서간의 거리를 계산하기 위한 함수.
    
    Args:
        state : 타겟과 커서의 좌표 정보
              : numpy array
        
    Returns:
        euclidean_distance : 타겟과 커서간의 유클리디안 거리
                           : float
    '''
    
    return np.sqrt((state[2] - state[0]) ** 2 + (state[3] - state[1]) ** 2)

def distance_reward(distance, sigma):
    '''
    거리를 Inverse Gaussian Function에 넣어 reward를 계산
    
    Args:
        distance : 타겟과 커서간의 유클리디안 거리
                 : float
        
        sigma : Inverse Gaussian Function의 variance
              : int
              
    Returns:
        reward : 강화학습에게 주어지는 reward
               : float
    '''
    
    return np.exp(-((distance ** 2) / (2 * (sigma **2))))

def hit(state, parameter):
    '''
    타겟 내 커서가 들어오면 타겟의 색을 빨간색으로 변환.
    
    Args:
        state : 타겟과 커서의 좌표 정보
              : numpy array
        
        parameter : 타겟의 크기를 호출하기 위한 파라미터 클래스
                  : class object
    
    Returns:
        Hit : 타겟 내 커서의 존재 여부
            : Boolean ( True : 타겟 내 커서가 존재 // False : 타겟 내 커서가 존재하지 않음 )
    '''
    
    return state[2] <= state[0] + 35 <= state[2] + parameter.target_diameter\
       and state[3] <= state[1] + 35 <= state[3] + parameter.target_diameter\
       and euclidean_distance(state) <= 35