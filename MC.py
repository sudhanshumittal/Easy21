from itertools import product
from mpl_toolkits.mplot3d import Axes3D
from random import random, randint
from sample.agent import agent
from sample.environment import Env
from sample.state import State
import logging
import matplotlib.pyplot as plt
import numpy as np

class player(agent):

    def __init__(self, No=100.):
        super(player, self).__init__()
        self.No = No
        self.Q = {}
        self.N = {}
        dealer_start = range(1, 11)
        player_states = range(1, 22)
        self.state_space = product(*[dealer_start, player_states])
        for state in self.state_space:
            for action in self.action_space:
                key = (state[0], state[1], action)
                self.Q[key] = 0.
                self.N[key] = 0
        
    def update_state_action_values(self, reward, visited_states_actions):
        for state, action in visited_states_actions:
            key = state + (action,)
            estimate = self.Q[key]
            error = (1. / self.N[key]) * (reward - estimate)
            self.Q[key] = estimate + error 
        # global Q
        # temp = (1. / n_visits)
        # temp[np.isinf(temp)] = 0
        # Q += temp * ep_visits * (reward - Q)
        # assert pl.Not np.isnan(np.sum(Q))
    
    def get_action(self, state):
        """returns action corresponding to a state using epsilon greedy policy"""
        def exploring():
            visits = self.N[state + (self.HIT,)] + self.N[state + (self.STICK,)]
            epsilon = self.No / (self.No + visits)
            return random() < epsilon
        
        action = None
        if exploring():
            action = randint(0, len(self.action_space) - 1)
        else:
            value_hit = self.Q[state + (self.HIT,)]
            value_stick = self.Q[state + (self.STICK,)]
            if value_hit >= value_stick:
                action = self.HIT
            else:
                action = self.STICK

        logging.debug("player action:" + str(action))
        return int(action)
    
    def visit(self, state, action):
        self.N[state + (action,)] += 1

#     def plot_reward(reward_arr):
#         t = range(1, len(reward_arr) + 1)
#         plt.plot(t, reward_arr)
#         plt.ylabel('rewards')
#         plt.show()
    
def plot(player):
    fig, ax1 = plt.subplots(1, 1, figsize=(8, 3), subplot_kw={'projection': '3d'})
    x = range(1, 11)  # dealer
    y = range(1, 22)  # player
    X, Y = np.meshgrid(x, y)
    Z = np.zeros((21, 10))
    for i in x:
        for j in y:
            policy = max(player.Q[(i, j, 0)], player.Q[(i, j, 1)])
            Z[j - 1][i - 1] = policy
    ax1.plot_wireframe(X, Y, Z)
    plt.tight_layout()
    plt.show()
    fig.savefig('./images/MC2.png')
    

if __name__ == '__main__':
    env = Env()
    pl = player()
    iterations = 10000
#     logging.basicConfig(filename='MC.log', level=logging.INFO)
    for _ in xrange(0, iterations):
        state_action_visited_in_epoch = []
        total_reward = 0
        curr_state = State()
        done = False
        while not done:
            action = pl.get_action(curr_state)
            pl.visit(curr_state, action)
            state_action_visited_in_epoch.append((curr_state, action))
            next_state, reward, done = env.step(curr_state, action)
            total_reward += reward
            logging.info(" state:" + str(curr_state) + " action:" + str(action))
            logging.info(" reward :" + str(reward) + " next state:" + next_state.__str__())
            curr_state = next_state
        logging.info("total reward :" + str(total_reward))
        pl.update_state_action_values(total_reward, state_action_visited_in_epoch)
    print pl.Q
#     plot(pl)
