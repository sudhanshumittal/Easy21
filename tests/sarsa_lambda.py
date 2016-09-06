from sample.environment import Env
from sample.sarsa_lambda_player import sarsa_lambda_player
from sample.utils import plot
import logging
if "__main__" == __name__:
    env = Env()
    player = sarsa_lambda_player()
    logging.basicConfig(level=logging.INFO)
    iterations = 100000
    player(env, iterations)
    plot(player)
