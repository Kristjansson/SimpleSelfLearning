import tictactoe as rules
from game import transitions
from mdp import MDP
from agent import QLearner

class AgentWrapper:
    def __init__(self, agent):
        self.agent = agent

    def __repr__(self):
        return self.__class__.__name__ + "(" + self.agent.__repr__() + ")"

    def __hash__(self):
        return hash(self.__class__) ^ hash(self.agent)

    def __eq__(self, other):
        return type(self) == type(other) and self.agent == other.agent

    def move(self, move):
        raise NotImplementedError("AgentWrapper.move is abstract!")


class TrainingWrapper(AgentWrapper):
    def update(self, *args):
        self.agent.update(*args)

    def move(self, state):
        return self.agent.choose_next_action(state)


class TestingWrapper(AgentWrapper):
    def update(self, *args):
        pass

    def move(self, state):
        return self.agent.optimal_action(state)


def run_for_episodes(mdp, episodes, players, debug=False):
    scores = {p : 0 for p in players}

    for ep in range(episodes):
        for transition in transitions(mdp, players):
            transition.player.update(transition.prev_state,
                                     transition.move,
                                     transition.post_opp_move_state,
                                     transition.reward)

            scores[transition.player] += transition.reward
        # switch who starts
        players = (*players[1:], players[0])
        
    if debug:
        print(scores)

    return scores


def epoch(mdp, training_episodes, testing_episodes, champion, contender, debug = False):
    champion = TestingWrapper(champion)
    contender = TrainingWrapper(contender)
    # train
    _ = run_for_episodes(mdp, training_episodes, (champion, contender))
    
    # evaluate
    champion = TestingWrapper(champion.agent)
    contender = TestingWrapper(contender.agent)
    return run_for_episodes(mdp, training_episodes, (champion, contender), debug)


def best_agent(results):
    ret = max(results, key = lambda k: results[k])
    
    if isinstance(ret, AgentWrapper):
        return ret.agent

    return ret


if __name__ == '__main__':
    num_epochs = 5000
    display_step = 50
    num_training_episodes = 100
    num_testing_episodes = 10

    mdp = MDP(rules)
    champion = QLearner()
    contender = QLearner(epsilon=0.5)


    for itr in range(num_epochs):
        results = epoch(mdp, 
                        num_training_episodes, 
                        num_testing_episodes, 
                        champion, 
                        contender)

        if (itr % display_step) == 0:
            champion.save('champion.p')
            print(itr, results)

        champion = best_agent(results)
        contender = champion.copy()


    with open('table.txt', 'w') as q_table_out:
        positions = {p:[] for p, m in champion.q_table}
        for p, m in champion.q_table:
            positions[p].append((m, champion.q_table[(p, m)]))

        for p, a in positions.items():
            q_table_out.write(str(p) + "\n")
            for m, v in a:
                q_table_out.write("\t" + str(m) + " ->" + str(v) + "\n")