from random import randint
import logging
class State(object):

    def __init__(self, dealer=None, player=None):
        if dealer is None and player is None:
            self.dealer = randint(1, 10)
            self.player = randint(1, 10)
        else:
            self.dealer = dealer
            self.player = player
        logging.info(self.__str__())

    def __str__(self):
        logging.info("""<dealer: %s player: %s>""" % (self.dealer, self.player))
        return """<dealer: %s player: %s>""" % (self.dealer, self.player)
    
    def __hash__(self):
        return hash((self.dealer, self.player))

    def __eq__(self, other):
        return (self.dealer, self.player) == (other.dealer, other.player)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)