class dealer(agent):
    def get_action(self, card_sum):
        action = self.HIT if card_sum <= 16 else self.STICK
        logging.debug("dealer action:"+ str(action))
        return action