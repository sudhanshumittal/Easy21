from sample.monte_carlo_player import monte_carlo_player
from sample.environment import Env
from sample.utils import plot
import logging
if "__main__" == __name__:
    env = Env()
    player = monte_carlo_player()
    logging.basicConfig(filename='MC.log', level=logging.INFO)
    iterations = 1
    player(env, iterations)
    plot(player)
