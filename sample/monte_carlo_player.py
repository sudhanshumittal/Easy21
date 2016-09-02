from agent import agent
from environment import Env
from state import State
from utils import epsilon_greedy_action, DefaultValueDict
import logging


class monte_carlo_player(agent):

    def __init__(self):
        super(monte_carlo_player, self).__init__()
        self.No = 100.
        self.Q = DefaultValueDict()
        self.N = DefaultValueDict()
        self.dealer_start = range(1, 11)
        self.player_states = range(1, 22)
#         state_space = product(*[self.dealer_start, self.player_states])
#         for state in state_space:
#             for action in self.action_space:
#                 key = State(state)+ (action,)
#                 self.Q[key] = 0.
#                 self.N[key] = 0
        
    def update_state_action_values(self, reward, visited_states_actions):
        for state, action in visited_states_actions:
            key = state + (action,)
            estimate = self.Q[key]
            error = (1. / self.N[key]) * (reward - estimate)
            self.Q[key] = estimate + error 
    
    def get_action(self, state):
        """returns action corresponding to a state using epsilon greedy policy"""
        visits = self.N[state + (self.HIT,)] + self.N[state + (self.STICK,)]
        epsilon = self.No / (self.No + visits)
        action_values = [self.Q[state + (action,)] for action in self.action_space]
        action = epsilon_greedy_action(self, epsilon, action_values)
        logging.debug("monte_carlo_player action:" + str(action))
        return int(action)
    
    def __call__(self, env, iterations=100):
        assert(isinstance(env, Env)), "invalid argument type: env"        
        for _ in xrange(0, iterations):
            state_action_visited_in_episode = []
            total_reward = 0
            curr_state = State()
            done = False
            while not done:
                action = self.get_action(curr_state)
                self.N[curr_state+(action,)] += 1
                state_action_visited_in_episode.append((curr_state, action))
                next_state, reward, done = env.step(curr_state, action)
                total_reward += reward
                logging.info(" state:" + str(curr_state) + " action:" + str(action) + " reward :" + str(reward) + " next state:" + next_state.__str__())
                curr_state = next_state
            logging.info("total reward :" + str(total_reward))
            self.update_state_action_values(total_reward, state_action_visited_in_episode)
        logging.info(self.Q)            


