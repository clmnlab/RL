########################################################################################
## Library import
########################################################################################
import os, sys, cv2, pickle
import numpy as np
import matplotlib.pyplot as plt
import pygame as G
sys.path.append('/home/lim/Artificial General Intelligence/Environment')

from parameters import *
from cursor import *
from target import *
from screen import *
from event import *
from env_util import *
from glob import glob
from PIL import Image

########################################################################################
## Class Definition
########################################################################################
class Path_visualization:
    '''
    게임 타겟의 경로에 관한 정보 클래스
    
    Attributes:
        directory : 타겟 경로가 위치하고 있는 폴더 위치
                  : str
                  
        name : 타겟 경로파일의 이름
             : str
             
    Methods:
        direction : 타겟 경로의 시작방향을 나타내기 위해 첫 10프레임 시각화
            
            Args:
                save_dir : 시각화 된 파일을 저장 할 경로
                         : str
                         
                name : 시각화 된 파일의 이름
                     : str
                     
        trajectory : 20개의 경로를 시각화
            
            Args:
                save_dir : 시각화 된 파일을 저장 할 경로
                         : str
                         
                name : 시각화 된 파일의 이름
                     : str
                     
        distribution : 타겟이 움직이는 각도를 histogram으로 시각화
            
            Args:
                save_dir : 시각화 된 파일을 저장 할 경로
                         : str
                         
                name : 시각화 된 파일의 이름
                     : str
                
    '''
    def __init__(self, directory, name):
        self._param = Parameters()
        self._screen = Screen()
        self._target = Target()
        self._cursor = Cursor()
        self._event = Event()
        
        self.name = name
        
        if '/' != directory[-1]:
            directory = directory + '/'
        else:
            pass

        self.path = np.load(directory + name)
        
        self.color_list = [(255, 0, 0), (125, 10, 10), (10, 255, 10), (10, 10, 255), (10, 125, 10), (10, 10, 125),
                      (125, 125, 10), (125, 10, 125), (10, 125, 125), (125, 125, 125)]
        
        print('=' * 50)
        print('Name : {}'.format(self.name))
        print('=' * 50)
        print('Shape : {}'.format(self.path.shape))

    def direction(self, save_dir, save_name):
        self._screen.overwrite()
        cur_list = self.path.tolist()
        
        tmp = 0
        
        for idx, (cur_x, cur_y) in enumerate(cur_list):
            if idx % 1500 < 10:
                G.draw.circle(self._screen.screen, G.Color(self.color_list[tmp]), (int(cur_x), int(cur_y)), 1, 3)
            if idx != 0 and idx % 1500 == 0:
                tmp += 1
            if tmp >= 10:
                tmp -= 10
        
        self._screen.flip()
        if '/' != save_dir[-1]:
            save_dir = save_dir + '/'
        else:
            pass
        
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        G.image.save(self._screen.screen, save_dir + save_name)
        
        print('=' * 50)
        print("Path direction image has been saved...")
        print('=' * 50)
        
    def trajectory(self, save_dir, save_name):
        self._screen.overwrite()
        cur_list = self.path.tolist()
        
        tmp = 0
        
        for idx, (cur_x, cur_y) in enumerate(cur_list):
            G.draw.circle(self._screen.screen, G.Color(self.color_list[tmp]), (int(cur_x), int(cur_y)), 1, 3)
            if idx != 0 and idx % 1500 == 0:
                tmp += 1
            if tmp >= 10:
                tmp -= 10
        
        self._screen.flip()
        if '/' != save_dir[-1]:
            save_dir = save_dir + '/'
        else:
            pass
        
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            
        G.image.save(self._screen.screen, save_dir + save_name)
        
        print('=' * 50)
        print("Path trajectory image has been saved...")
        print('=' * 50)
    
    def distribution(self,save_dir, save_name):
        if '/' != save_dir[-1]:
            save_dir = save_dir + '/'
        else:
            pass
        
        prev_x = self.path[:, 0]
        prev_y = self.path[:, 1]
        
        curr_x = np.zeros_like(prev_x)
        curr_y = np.zeros_like(prev_y)
        
        for idx in range(0, len(prev_x)-1):
            curr_x[idx+1] = prev_x[idx]
            curr_y[idx+1] = prev_y[idx]
            
        dt_x = (prev_x - curr_x).reshape(-1, 1)
        dt_y = (prev_y - curr_y).reshape(-1, 1)
        
        dt = np.concatenate([dt_x, dt_y], axis=1)[1:]
        
        dt_tan = []
        for idx in range(len(dt)):
            if dt[idx][0] >= 0:
                dt_tan.append(np.rad2deg(np.arctan(dt[idx][1] / dt[idx][0])))
            elif dt[idx][0] < 0:
                dt_tan.append(180 + np.rad2deg(np.arctan(dt[idx][1] / dt[idx][0])))
        dt_degree = np.array(dt_tan).astype('int')
        dt_degree += 90
        
        plt.figure(figsize=(22, 8))
        plt.hist(dt_degree, bins=36)
        plt.xticks(list(range(0, 361, 10)))
        plt.savefig(save_dir + save_name)
        plt.close()
        print('=' * 50)
        print("Path distribution image has been saved...")
        print('=' * 50)
        
########################################################################################
## Class Definition
########################################################################################
class Cursor_visualization:
    '''
    피험자의 조이스틱 움직임을 시각화하기 위한 클래스
    
    Attributes:
        path_dir :  경로 파일 폴더
        exp_dir : 피험자 실험 데이터 폴더
        subj : 피험자 번호
    
    Methods:
        trajectory : 타겟과 커서를 그린 후 저장
            
            Args:
                save_dir : 이미지를 저장 할 폴더
                         : str
    '''
    def __init__(self, path_dir, exp_dir, subj):
        self._param = Parameters()
        self.subj = subj
        
        if '/' != path_dir[-1]:
            path_dir = path_dir + '/'
        else:
            pass
        
        self.path = np.load(glob(path_dir+'*.npy')[0])
        
        path = []
        for idx in range(20):
            for j in range(1500 * idx, 1500 * idx + 1465):
                path.append(self.path[j])
        self.path = np.array(path)
            
        if '/' != exp_dir[-1]:
            exp_dir = exp_dir + '/'
        else:
            pass
        
        self.run_list = glob(exp_dir + subj + '/' + '*.pkl')
    
    def trajectory(self, save_dir):
        self.run_list = self.run_list
        
        for num, run in enumerate(self.run_list):
            if '/' != save_dir[-1]:
                run_dir = save_dir + '/' + 'Run_{0:02d}'.format(num+1) + '/'
            else:
                run_dir = save_dir + 'Run_{0:02d}'.format(num+1) + '/'

            if not os.path.exists(run_dir):
                os.makedirs(run_dir)
                
            with open(run, 'rb') as f:
                exp = pickle.load(f)
            exp = exp['cursor']
            
            clock_tick(self._param.hertz)
            _screen = Screen()
            _target = Target()
            _cursor = Cursor()
            _event = Event()
            color_list = [(0, 0, 0), (78, 112, 189)]
            cur_list = self.path.tolist()
            
            G.event.pump()
            _screen.screen.fill(self._param.white)
            
            for trial in range(1, 21, 1):
                for idx in range(1465 * (trial - 1), 1465 * trial):
                    G.draw.circle(_screen.screen, G.Color(color_list[0]), (int(cur_list[idx][0]), int(cur_list[idx][1])), 3, 0)
                    G.draw.circle(_screen.screen, G.Color(color_list[1]), (int(exp[idx][0] - 35), int(exp[idx][1] - 35)), 3, 0)
                
                _screen.flip()
                
                string_image = G.image.tostring(_screen.screen, 'RGB')
                temp_surf = G.image.fromstring(string_image, (self._param.width, self._param.height), 'RGB')
                tmp = G.surfarray.array3d(temp_surf)
                tmp = tmp.transpose((1, 0, 2))
                
                plt.imshow(tmp)
                plt.axis('off')
                plt.text(20, 0, '- : target')
                plt.text(20, 70, '- : cursor', c='b')
                trial = '{0:02d}'.format(trial)
                plt.savefig(f'{run_dir}trial_{trial}.png', dpi = 300)
                _screen.screen.fill(self._param.white)
                
        plt.close()        

########################################################################################
## Class Definition
########################################################################################
class Human_video:
    '''
    피험자의 조이스틱 움직임을 영상화하기 위한 클래스
    
    Attributes:
        exp_dir : 피험자 실험 데이터 폴더
        subj : 피험자 번호
    
    Methods:
        save_video : 타겟과 커서를 그린 후 저장
            
            Args:
                run_list : Run 번호
                         : list // (e.g, ['01'])
                         
                trial_num : trial 번호
                          : int // (e.g, 1)
    '''
    def __init__(self, exp_path, subj):
        exp_path = exp_path + '/' if '/' != exp_path[-1] else exp_path
        subj = subj + '/' if '/' != subj[-1] else subj
        
        self.exp_path = exp_path
        self.subj = subj
    
    def save_video(self, run_list, trial_num):
        for run in run_list:
            if not os.path.exists(self.exp_path + self.subj + 'Run_{0:02d}'.format(int(run))):
                os.makedirs(self.exp_path + self.subj + 'Run_{0:02d}'.format(int(run)))
            
            with open(self.exp_path + self.subj + 'behavior_data_{}.pkl'.format(int(run)), 'rb') as f:
                exp = pickle.load(f)
            
            G.init()
            screen = G.display.set_mode([1920, 1080])
            frame = []
            
            for trial in range(trial_num, trial_num + 1, 1):
                for idx in range(1465 * (trial-1), 1465 * (trial)):
                    screen.fill(G.Color(0, 0, 0))
                    target_rect = Rect(int(exp['target'][idx][0]), int(exp['target'][idx][1]), 70, 70)
                    
                    if 'adap' in self.subj:
                        G.draw.ellipse(screen, G.Color(0, 0, 255), target_rect, 0)
                    else:
                        G.draw.ellipse(screen, G.Color(128, 128, 128), target_rect, 0)
                    
                    if exp['hit'][idx][0] == 1:
                        G.draw.ellipse(screen, G.Color(255, 0, 0), target_rect, 0)
                    
                    G.draw.line(screen, G.Color(255, 255, 255), (int(exp['cursor'][idx][0]) - 10, int(exp['cursor'][idx][1])), (int(exp['cursor'][idx][0]) + 10, int(exp['cursor'][idx][1])), 3)
                    G.draw.line(screen, G.Color(255, 255, 255), (int(exp['cursor'][idx][0]), int(exp['cursor'][idx][1]) - 10), (int(exp['cursor'][idx][0]), int(exp['cursor'][idx][1]) + 10), 3)
                    G.display.flip()
                    G.image.save(screen, 'tmp.BMP')
                    png = Image.open('./tmp.BMP')
                    png = png.convert('RGBA')
                    png.load()
                    
                    
                    background = Image.new('RGB', png.size, (255, 255, 255))
                    background.paste(png, mask = png.split()[3])
                    frame.append(background)
                    
                frame_array = []
                for idx in range(len(frame)):
                    frame_array.append(cv2.cvtColor(np.array(frame[idx]), cv2.COLOR_RGB2BGR))
                
                height, width, layers = frame_array[0].shape
                size = (width, height)
                print(size)
                
                video = cv2.VideoWriter(self.exp_path + self.subj + 'Run_{0:02d}'.format(int(run)) + '/' + 'trial_{0:02d}.mp4'.format(trial), fourcc=0x7634706d, fps=60, frameSize=size)
                
                for idx in range(1465):
                    video.write(frame_array[idx])
                video.release()
            
            G.quit()
            os.system('rm -rf ./tmp.BMP')
                                

########################################################################################
## Class Definition
########################################################################################
class RL_video:
    '''
    학습된 강화학습을 영상화하기 위한 클래스
    
    Attributes:
        action_dir : 강화학습 모델이 저장된 폴더
        epoch : 강화학습 모델의 action이 저장된 이름
    
    Methods:
        save_video : 타겟과 커서를 그린 후 저장
            
            Args:
                run_list : Run 번호
                         : list // (e.g, ['01'])
                         
                trial_num : trial 번호
                          : int // (e.g, 1)
    '''
    def __init__(self, action_path, epoch):
        action_path = action_path + '/' if '/' != action_path[-1] else action_path
        name = name + '/' if '/' != name[-1] else name
        
        self.exp_path = exp_path
        self.subj = subj
    
    def save_video(self, run_list, trial_num):
        for run in run_list:
            if not os.path.exists(self.exp_path + self.subj + 'Run_{0:02d}'.format(int(run))):
                os.makedirs(self.exp_path + self.subj + 'Run_{0:02d}'.format(int(run)))
            
            with open(self.exp_path + self.subj + 'behavior_data_{}.pkl'.format(int(run)), 'rb') as f:
                exp = pickle.load(f)
            
            G.init()
            screen = G.display.set_mode([1920, 1080])
            frame = []
            
            for trial in range(trial_num, trial_num + 1, 1):
                for idx in range(1465 * (trial-1), 1465 * (trial)):
                    screen.fill(G.Color(0, 0, 0))
                    target_rect = Rect(int(exp['target'][idx][0]), int(exp['target'][idx][1]), 70, 70)
                    
                    if 'adap' in self.subj:
                        G.draw.ellipse(screen, G.Color(0, 0, 255), target_rect, 0)
                    else:
                        G.draw.ellipse(screen, G.Color(128, 128, 128), target_rect, 0)
                    
                    if exp['hit'][idx][0] == 1:
                        G.draw.ellipse(screen, G.Color(255, 0, 0), target_rect, 0)
                    
                    G.draw.line(screen, G.Color(255, 255, 255), (int(exp['cursor'][idx][0]) - 10, int(exp['cursor'][idx][1])), (int(exp['cursor'][idx][0]) + 10, int(exp['cursor'][idx][1])), 3)
                    G.draw.line(screen, G.Color(255, 255, 255), (int(exp['cursor'][idx][0]), int(exp['cursor'][idx][1]) - 10), (int(exp['cursor'][idx][0]), int(exp['cursor'][idx][1]) + 10), 3)
                    G.display.flip()
                    G.image.save(screen, 'tmp.BMP')
                    png = Image.open('./tmp.BMP')
                    png = png.convert('RGBA')
                    png.load()
                    
                    
                    background = Image.new('RGB', png.size, (255, 255, 255))
                    background.paste(png, mask = png.split()[3])
                    frame.append(background)
                    
                frame_array = []
                for idx in range(len(frame)):
                    frame_array.append(cv2.cvtColor(np.array(frame[idx]), cv2.COLOR_RGB2BGR))
                
                height, width, layers = frame_array[0].shape
                size = (width, height)
                print(size)
                
                video = cv2.VideoWriter(self.exp_path + self.subj + 'Run_{0:02d}'.format(int(run)) + '/' + 'trial_{0:02d}.mp4'.format(trial), fourcc=0x7634706d, fps=60, frameSize=size)
                
                for idx in range(1465):
                    video.write(frame_array[idx])
                video.release()
            
            G.quit()
            os.system('rm -rf ./tmp.BMP')
            
                            
                               