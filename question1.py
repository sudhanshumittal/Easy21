from sample.monte_carlo_player import monte_carlo_player
from sample.environment import Env
from sample.utils import plot
import logging
logging.basicConfig(filename='easy21.log', level=logging.INFO)
if "__main__" == __name__:
    env = Env()
    player = monte_carlo_player()
    iterations = 1
    player(env, iterations)
    plot(player)
