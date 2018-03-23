import tictactoe as rules
from game import episode
from agent import QLearner

class AgentWrapper:
    def __init__(self, agent):
        self.agent = agent

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
    for ep in range(episodes):
        game = episode(mdp, players)
        for step in game:
            step.player.agent.update(step.prev_state, 
                                     step.move, 
                                     step.new_state, 
                                     step.reward)
        yield (step.player.agent, step.reward)
        players = (*players[1:], players[0])
        
        if debug:
            print(step.new_state)


def epoch(mdp, training_episodes, testing_episodes, champion, contender):
    champion = TestingWrapper(champion)
    contender = TrainingWrapper(contender)
    # train
    for _ in run_for_episodes(mdp, training_episodes, (champion, contender)):
        pass

    # evaluate
    contender = TestingWrapper(contender.agent)
    return list(run_for_episodes(mdp, 
                                 testing_episodes, 
                                 (champion, contender), 
                                 debug = False))


def best_agent(results, champion, contender, debug=False):
    name_to_agent = {
        champion.name: champion,
        contender.name: contender
    }

    name_to_score = {
        champion.name: 0,
        contender.name: 0
    }

    for result in results:
        name_to_score[result[0].name] += result[1]

    if debug:
        print(name_to_score)

    return max(name_to_agent.items(), key = lambda x: name_to_score[x[0]])[1]


num_epochs = 10
num_training_episodes = 100
num_testing_episodes = 10

mdp = rules.TicTacToe_MDP()
champion = QLearner(mdp)
contender = QLearner(mdp)


for itr in range(num_epochs):
    results = epoch(mdp, 
                    num_training_episodes, 
                    num_testing_episodes, 
                    champion, 
                    contender)

    champion = best_agent(results, champion, contender, debug=True)
    contender = champion.copy()

champion.save('champion.p')
