from itertools import product
from mpl_toolkits.mplot3d.axes3d import Axes3D
from numpy import argmax, meshgrid, zeros
from random import random, randint
import matplotlib.pyplot as plt

class DefaultValueDict(dict):
    """extends the python dictionary to return 0.0 when a key is missing.
    This is helpful in Easy21 because there are a lot of terminal states 
    for which Q values need not be separately stored. Moreover, it also 
    implicitly initializes Q value as 0.0 """
    def __missing__(self, key):
        return 0.

def epsilon_greedy_action(self, epsilon, action_values):
    action = None
    exploring = random() < epsilon
    if exploring:
        action = randint(0, len(self.action_space) - 1)
    else:
        action = argmax(action_values)
    return action

def plot(player):
    fig = plt.figure()
    ax = Axes3D(fig)
    x = player.dealer_start
    y = player.player_states
    X, Y = meshgrid(x, y)
    Z = zeros((21, 10))
    state_space = product(*[player.dealer_start, player.player_states])
    for state in state_space:
        policy = max([player.Q[state+ (action,)] for action in player.action_space])
        Z[state[1]-1][state[0]-1] = policy
    ax.plot_wireframe(X, Y, Z)
    plt.show()
    
def plot2d(ip_dict):
    assert(isinstance(ip_dict, dict))
    keys = ip_dict.keys()
    values = ip_dict.values()
    plt.scatter(keys, values)
    plt.show()
    
def calculate_MSE(Q1, Q2):
    dealer_start = range(1, 11)
    player_states = range(1, 22)
    state_space = product(*[dealer_start, player_states])
    MSE = 0.
    for state in state_space:
        for action in [0,1]:
            key = state + (action,)
            sqErr = pow(Q1[key] - Q2[key],2)
            MSE +=sqErr
    return MSE