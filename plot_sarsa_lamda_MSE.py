from sample.environment import Env
from sample.monte_carlo_player import monte_carlo_player
from sample.sarsa_lambda_player import sarsa_lambda_player
from sample.utils import calculate_MSE, plot2d
if "__main__" == __name__:
    env = Env()
    mcplayer = monte_carlo_player()
    print "running monte carlo player with 50000 iterations"
    mcplayer(env,iterations = 50000)
    Q1 = mcplayer.Q
    mse = {}
    for lmbda in range(0,11):
        lmbda = lmbda/10.
        print "running sarsa lambda player with 1000 iterations and lambda ", lmbda
        player = sarsa_lambda_player(lmbda)
        player(env, iterations = 1000)
        Q2 = player.Q
        mse[lmbda] = calculate_MSE(Q1,Q2)
    print mse
    plot2d(mse)