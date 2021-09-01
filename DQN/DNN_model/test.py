import collections
import random
import numpy as np

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

from Pkg.Denovo_DQN import Denovo_Env

# Hyperparameters
learning_rate = 0.001
gamma = 0.98
buffer_limit = 50000
batch_size = 512


class ReplayBuffer():
    def __init__(self):
        self.buffer = collections.deque(maxlen=buffer_limit)

    def put(self, transition):
        self.buffer.append(transition)

    def sample(self, n):
        mini_batch = random.sample(self.buffer, n)
        s_lst, a_lst, r_lst, s_prime_lst, done_mask_lst = [], [], [], [], []

        for transition in mini_batch:
            s, a, r, s_prime, done_mask = transition
            s_lst.append(s)
            a_lst.append([a])
            r_lst.append([r])
            s_prime_lst.append(s_prime)
            done_mask_lst.append([done_mask])

        return torch.tensor(s_lst, dtype=torch.float), torch.tensor(a_lst), \
               torch.tensor(r_lst), torch.tensor(s_prime_lst, dtype=torch.float), \
               torch.tensor(done_mask_lst)

    def size(self):
        return len(self.buffer)


class Qnet(nn.Module):
    def __init__(self):
        super(Qnet, self).__init__()
        self.fc1 = nn.Linear(4, 32)
        self.fc2 = nn.Linear(32, 64)
        self.fc3 = nn.Linear(64, 128)
        self.fc4 = nn.Linear(128, 128)
        self.fc5 = nn.Linear(128, 8)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = F.relu(self.fc4(x))
        x = self.fc5(x)
        return x

    def sample_action(self, obs, epsilon):
        out = self.forward(obs)
        coin = random.random()
        if coin < epsilon:
            return random.randint(0, 7)
        else:
            return out.argmax().item()


def train(q, q_target, memory, optimizer):
    for i in range(10):
        s, a, r, s_prime, done_mask = memory.sample(batch_size)

        q_out = q(s)
        q_a = q_out.gather(1, a)
        max_q_prime = q_target(s_prime).max(1)[0].unsqueeze(1)
        target = r + gamma * max_q_prime * done_mask
        loss = F.smooth_l1_loss(q_a.float(), target.float())

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()


q = torch.load('./DNN_model/q.pt')
q_target = torch.load('./DNN_model/q_target.pt')
print(q.eval())
print(q_target.eval())
memory = ReplayBuffer()
for x in q.parameters():
    print(x)

env = Denovo_Env()
print_interval = 20
score = 0.0
optimizer = optim.Adam(q.parameters(), lr=learning_rate)

for n_epi in range(80000, 100000):
    epsilon = max(0.01, 0.8 - 0.01 * (n_epi / 1000))  # Linear annealing from 8% to 1%
    done = False
    s = env.reset().copy()
    count = 0
    while not done:

        a = q.sample_action(torch.from_numpy(np.array(s)).float(), epsilon)
        s_prime, r, done, info = env.step(a)
        env.render()
        done_mask = 0.0 if done else 1.0
        s = s_prime.copy()
        score += r
        count += 1

        if done:
            break

    if n_epi % print_interval == 0 and n_epi != 0:
        q_target.load_state_dict(q.state_dict())
        print("n_episode :{}, score : {:.1f}, n_buffer : {}, eps : {:.1f}%".format(
            n_epi, score / print_interval, memory.size(), epsilon * 100))
        print(count / print_interval)
        score = 0.0
        count = 0.0

env.close()

torch.load('')
