import collections
import random
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

# Hyper Parameters

learning_rate = 0.001
discount_factor = 0.98
buffer_limit = 50000
batch_size = 32

# Define ReplayBuffer
# put : list
# sample : int

class ReplayBuffer:
    def __init__(self):
        self.buffer = collections.deque(maxlen = buffer_limit)

    def put(self, transition):
        self.buffer.append(transition)

    def sample(self, n):
        mini_batch = random.sample(self.buffer, n)
        s_list, a_list, r_list, s_prime_list, done_mask_list = [], [], [], [], []

        for transition in mini_batch:
            s, a, r, s_prime, done_mask = transition
            s_list.append(s)
            a_list.append(a)
            r_list.append(r)
            s_prime_list.append(s_prime)
            done_mask_list.append(done_mask)

        return  torch.tensor(s_list, dtype = torch.float), \
                torch.tensor(a_list), torch.tensor(r_list), \
                torch.tensor(s_prime_list, dtype = torch.float), \
                torch.tensor(done_mask_list)

    def size(self):
        return len(self.buffer)


class DQN(nn.Module):
    def __init__(self, in_channels = 4, n_actions = 9):
        super(DQN, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, 32, kernel_size = 8, stride = 4)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(16, 64, kernel_size = 4, stride = 2)
        self.bn2 = nn.BatchNorm2d(64)
        self.conv3 = nn.Conv2d(64, 64, kernel_size = 3, stride = 1)
        self.bn3 = nn.BatchNorm2d(64)
        self.fc4 = nn.Linear(7 * 7 * 64, 512)
        self.head = nn.Linear(512, n_actions)

    def forward(self, x):
        x = x.float() / 255
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))
        x = F.relu(self.fc4(x.view(x.size(0), -1)))
        return self.head(x)

