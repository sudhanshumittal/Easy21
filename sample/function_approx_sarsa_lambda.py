from itertools import product
from mpl_toolkits.mplot3d.axes3d import Axes3D
from sample.sarsa_lambda_player import sarsa_lambda_player
from sample.state import State
from sample.utils import epsilon_greedy_action
import logging
import matplotlib.pyplot as plt
import numpy as np


class function_approx_sarsa_lambda(sarsa_lambda_player):
    def __init__(self, lmbd=0.1):
        super(function_approx_sarsa_lambda, self).__init__(lmbd);
        self.W = np.zeros(36, dtype=np.float64)
        self.epsilon = 0.05
        self.alpha = 0.01
        self.dealer_cube = [range(1, 5), range(4, 8), range(7, 11)]
        self.player_cube = [range(1, 7), range(4, 10), range(7, 13), range(10, 16), range(13, 19), range(16, 22)]
        self.action_cube = [[0], [1]]
    
    def Q_fn(self, state, action):
        features = self.get_input_features(state, action)
        return np.dot(features, self.W)
        
    def get_input_features(self, state, action):
        dealer_vec = np.array([1. if state.dealer() in cube else 0. for cube in self.dealer_cube])
        player_vec = np.array([1. if state.player() in cube else 0. for cube in self.player_cube])
        action_vec = np.array([1. if action in cube else 0. for cube in self.action_cube])
        feature_vector = (dealer_vec.reshape(-1, 1)*player_vec).reshape(-1,1)
        feature_vector = (feature_vector*action_vec).flatten()
        return feature_vector
    
    def update_state_action_values(self, state_actions_visited, TD_error, E):
        for state, action in state_actions_visited:
            self.W += self.alpha * TD_error * E[state + (action,)]
    
    def increment_eligibility_trace(self, E, state, action):
        grad = self.get_input_features(state, action)
        E[state + (action,)] += grad

    def get_td_error(self, reward, curr_state, curr_action, next_state, next_action):
        Q_t_plus_1 = self.Q_fn(next_state, next_action)
        Q_t = self.Q_fn(curr_state, curr_action)
        return reward + self.gamma*Q_t_plus_1 - Q_t
                
    def get_action(self, state):
        action_values = [self.Q_fn(state, self.HIT), self.Q_fn(state, self.STICK)]
        action = epsilon_greedy_action(self.epsilon, action_values)
        logging.debug("action:" + str(action))
        return int(action)

    def plot_optimal_value(self):
        fig = plt.figure()
        ax = Axes3D(fig)
        x = self.dealer_start
        y = self.player_states
        X, Y = np.meshgrid(x, y)
        Z = np.zeros((21, 10))
        state_space = product(*[self.dealer_start, self.player_states])
        for state in state_space:
            policy = max([self.Q_fn(State(state), action) for action in self.action_space])
            Z[state[1] - 1][state[0] - 1] = policy
        ax.plot_wireframe(X, Y, Z)
        plt.show()
