from collections import OrderedDict
from sample.environment import Env
from sample.monte_carlo_player import monte_carlo_player
from sample.sarsa_lambda_player import sarsa_lambda_player
from sample.utils import calculate_MSE, plot2d
import logging

# logging.basicConfig(level=logging.INFO)
def plot_lambda_vs_MSE(optimal_Q):         
    mse = OrderedDict()
    iterations = 10000
    for lmbda in range(0, 11):
        lmbda = lmbda / 10.
        print "running sarsa lambda player with ", iterations, " iterations and lambda=", lmbda
        player = sarsa_lambda_player(lmbda)
        player(env, iterations)
        Q2 = player.Q
        mse[lmbda] = calculate_MSE(optimal_Q, Q2)
    plot2d([mse.keys()], [mse.values()])
    
def plot_learning_curve(optimal_Q):
    x = []; y = []
    iterations = 100000
    for lmbda in [0, 1]:
        x.append([]); y.append([])
        print "running sarsa lambda player with ", iterations, " iterations and lambda=", lmbda
        player = sarsa_lambda_player(lmbda)
        for iter in range(1, iterations+1):
            player(env, 1)
            mseNow = calculate_MSE(optimal_Q, player.Q)
            x[-1].append(iter); y[-1].append(mseNow)
    plot2d(x, y)
    
if "__main__" == __name__:
    env = Env()
    mcplayer = monte_carlo_player()
    iterations = 50000
    print "running monte carlo player with iterations=", iterations
    mcplayer(env, iterations)
    optimal_Q = mcplayer.Q
    plot_lambda_vs_MSE(optimal_Q)
#     plot_learning_curve(optimal_Q)
