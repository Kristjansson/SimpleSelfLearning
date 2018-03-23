import random
import pickle as p
import time

def ids():
    i = 100000
    while True:
        yield i
        i += 1
        if i > 999999:
            i = 100000

class QLearner:
    id_gen = ids()

    def __init__(self, mdp, q_table=None, epsilon=0.1, gamma=0.9, learning_rate=0.5, name=None):
        self.mdp = mdp
        self.q_table = q_table or {}
        self.epsilon = epsilon
        self.gamma = gamma
        self.learning_rate = learning_rate
        self.name = name or next(self.id_gen)

    def Q(self, state, action):
        return self.q_table.get((state, action), 0)

    def choose_next_action(self, state):
        """Given a state this returns the agent's choice for the next action, using an epsilon-greedy strategy."""
        if random.random() < self.epsilon:
            return random.choice(state.possible_moves())
        else:
            return self.optimal_action(state)

    def optimal_action(self, state):
        """Given a state, this returns the agent's choice for the optimal next action. This in affect is the
        learned policy."""
        return max(state.possible_moves(),
                   key=lambda a: self.Q(state, a))

    def update(self, prev_state, action, new_state, reward):
        new_action = self.optimal_action(new_state)

        new_q_val = ((1 - self.learning_rate) * self.Q(prev_state, action) + 
                     self.learning_rate * (reward + self.gamma * self.Q(new_state, new_action)))

        self.q_table[(prev_state, action)] = new_q_val

    def save(self, filename):
        with open(filename, 'wb') as save_file:
            p.dump(self, save_file)

    def load(filename):
        with open(filename, 'rb') as load_file:
            return p.load(load_file)

    def copy(self, new_name=None):
        return QLearner(mdp=self.mdp, 
            q_table={**self.q_table}, 
            epsilon=self.epsilon, 
            gamma=self.gamma, 
            learning_rate=self.learning_rate, 
            name = new_name or next(self.id_gen))

    def __eq__(self, other):
        return type(self) == type(other) and self.name == other.name