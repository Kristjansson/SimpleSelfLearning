import random
import pickle as p
import time

def ids():
    i = 1
    while True:
        yield str(i)
        i += 1

class Agent:
    id_gen = ids()

    def __eq__(self, other):
        return type(self) == type(other) and self.name == other.name

    def __repr__(self):
        return "Agent: " + self.name

    def __hash__(self):
        return hash(self.name)

    def save(self, filename):
        with open(filename, 'wb') as save_file:
            p.dump(self, save_file)

    def load(filename):
        with open(filename, 'rb') as load_file:
            return p.load(load_file)

class Minimaxer(Agent):
    def __init__(self, model, depth = 3, name=None):
        self.model = model
        self.depth = depth
        self.name = name or next(self.id_gen)

    def minimax(self, state, prev_state = None, prev_move = None, minOrMax=(min, max), pm = 1):
        if state.game_over():
            ret =  pm*self.model.reward(prev_state, prev_move, state)
            return ret
        else:
            fun = minOrMax[0]
            ret =  fun(self.minimax(state.move(move), state, move, (minOrMax[1], minOrMax[0]), -1*pm)
                       for move in state.possible_moves())
            return ret

    def choose_next_action(self, state):
        return self.optimal_action(state)

    def optimal_action(self, state):
        return max((move for move in state.possible_moves()),
                   key=lambda move, state=state: self.minimax(state.move(move)))

    def update(self, *args):
        pass

    def copy(self, new_name=None):
        return Minimaxer(self.model, 
                         self.depth,
                         new_name or next(self.id_gen))

class QLearner(Agent):
    def __init__(self, q_table=None, epsilon=0.1, gamma=0.9, learning_rate=0.5, name=None):
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

    def copy(self, new_name=None):
        return QLearner(q_table={**self.q_table}, 
            epsilon=self.epsilon, 
            gamma=self.gamma, 
            learning_rate=self.learning_rate, 
            name = new_name or next(self.id_gen))