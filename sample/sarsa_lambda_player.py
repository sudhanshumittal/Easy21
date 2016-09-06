from agent import agent
from environment import Env
from state import State
from utils import epsilon_greedy_action, DefaultValueDict
import logging

class sarsa_lambda_player(agent):
    def __init__(self, lmbd=0.1):
        super(sarsa_lambda_player, self).__init__()
        self.lmbd = lmbd
        self.gamma = 1.
        self.No = 100.
        self.Q = DefaultValueDict()
        self.N = DefaultValueDict()
        self.dealer_start = range(1, 11)
        self.player_states = range(1, 22)
        
    def update_state_action_values(self, state_actions_visited, TD_error, E):
        for state, action in state_actions_visited:
            key = state + (action,)
            step_size = (1. / self.N[key])
            self.Q[key] += step_size * TD_error * E[key]
            
    def decay_eligibility_traces(self, E):
        for key in E.keys():
            E[key] *= self.gamma * self.lmbd
            
    def get_action(self, state):
        visits = self.N[state + (self.HIT,)] + self.N[state + (self.STICK,)]
        epsilon = self.No / (self.No + visits)
        action_values = [ self.Q[state + (action,)] for action in self.action_space]
        action = epsilon_greedy_action(epsilon, action_values)
        logging.debug("sarsa_lambda_player action:" + str(action))
        return int(action)
    def get_td_error(self, reward, curr_state, curr_action, next_state, next_action):  # override
        return reward + self.Q[next_state + (next_action,)] - self.Q[curr_state + (curr_action,)]
    def increment_eligibility_trace(self, E, state, action):
        E[state + (action,)] += 1.
    def __call__(self, env, iterations=1):
        assert(isinstance(env, Env)), "invalid argument type: env"
        for _ in xrange(0, iterations):
            E = DefaultValueDict()
            state_action_visited_in_episode = []
            curr_state = State()
            curr_action = self.get_action(curr_state)
            done = False
            while not done:
                self.N[curr_state + (curr_action,)] += 1
                state_action_visited_in_episode.append((curr_state, curr_action))
                next_state, reward, done = env.step(curr_state, curr_action)
                next_action = self.get_action(next_state)
                logging.info(" state:" + str(curr_state) + " action:" + str(curr_action) + \
                             " reward :" + str(reward) + " next state:" + next_state.__str__()\
                             + "next action:" + str(next_action))
                TD_error = self.get_td_error(reward, curr_state, curr_action, next_state, next_action)
                self.increment_eligibility_trace(E, curr_state, curr_action)
                self.update_state_action_values(state_action_visited_in_episode, TD_error, E)
                self.decay_eligibility_traces(E)
                curr_state = next_state
                curr_action = next_action
                
        logging.info(self.Q)            
