class MDP:
    def __init__(self, rules):
        self.rules = rules

    def initial_state(self):
        return self.rules.initial_state()

    def operators(self, state):
        return state.possible_moves()

    def reward(self, prev_state, move, new_state, opp_move=None, opp_state=None):
        """For two player games the reward function is more complex. We want to be 
        rewarded if we do something good, but we should also be penalized if our
        opponent does something good. Also, because if we win there will not be an
        opponent state, we have to be careful. """
        penalties = 0
        if opp_move is not None and opp_state is not None:
            penalties = self.rules.penalties(new_state, opp_move, opp_state)
        return self.rules.rewards(prev_state, move, new_state) + penalties