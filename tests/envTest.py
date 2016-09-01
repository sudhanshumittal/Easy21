# main routine for debugging
from sample import * 
import logging

logging.basicConfig(filename='environment.log', level=logging.DEBUG)
HIT = 0
STICK = 1
GAMMA = 1.
def test_always_stick():
    logging.debug("playing with always stick policy")
    a = STICK
    e = environment.Env()
    s = state.State()
    done = False
    while not done:
        s, r, done = e.step(s, a)
    print "state:", s, "reward =", r
def test_always_hit():
    logging.debug("playing with always hit policy")
    e = environment.Env()
    s = state.State()
    a = HIT
    done = False
    while not done:
        s, r, done = e.step(s, a)
    print "state:", s, "reward =", r
if __name__ == '__main__':
    logging.debug("testing environment")
    test_always_hit()
    test_always_stick()
