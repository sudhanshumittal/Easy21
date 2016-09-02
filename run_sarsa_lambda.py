from sample.environment import Env
from sample.sarsa_lambda_player import sarsa_lambda_player
from sample.utils import plot
if "__main__" == __name__:
    env = Env()
    player = sarsa_lambda_player()
#     logging.basicConfig(filename='sarsa.log', level=logging.DEBUG)
    iterations = 1
    player(env, iterations)
    plot(player)
