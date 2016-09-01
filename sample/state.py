from random import randint
import logging
__author__ = 'sudhanshu mittal'

class State(tuple):
    
    @staticmethod
    def __new__(cls, *args):
        if not args:
            dealer = randint(1, 10)
            player = randint(1, 10)
            obj = super(State, cls).__new__(cls, (dealer, player))
        else:
            assert(len(args) == 2), "invalid arguments passed"
            obj = super(State, cls).__new__(cls, args)
        logging.debug("""<dealer: %s player: %s>""" % (obj[0], obj[1]))
        return obj    
    
    def dealer(self):
        return self[0]

    def player(self):
        return self[1]
     
 
    def __str__(self):
        return """<dealer: %s player: %s>""" % (self[0], self[1])
     
    def __hash__(self):
        return hash((self.dealer, self.player))
 
    def __eq__(self, other):
        return (self.dealer, self.player) == (other.dealer, other.player)
 
    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)
