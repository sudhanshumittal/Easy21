from agent import agent;
class dealer(agent):
    def get_action(self, card_sum):
        return self.HIT if card_sum <= 16 else self.STICK
