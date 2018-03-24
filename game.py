"""A reusable framework for iterating through games"""

from collections import namedtuple

GameStep = namedtuple('GameStep', ['prev_state', 'move', 'new_state', 'player'])
MDPStep = namedtuple('MDPStep', ['prev_state', 'move', 'post_opp_move_state', 'player', 'reward'])

def episode(mdp, players):
    curr_state = mdp.initial_state()
    while not curr_state.game_over():
        curr_player = players[0]
        move = curr_player.move(curr_state)
        new_state = curr_state.move(move)
            
        # This yields the player that moved from previous state to new_state
        yield GameStep(prev_state = curr_state, 
                       move = move,
                       new_state = new_state,
                       player = curr_player)

        curr_state = new_state
        players = (*players[1:], players[0])

def transitions(mdp, players):
    game = episode(mdp, players)
    prev = next(game)
    for step in game:
        reward = mdp.reward(prev.prev_state, 
                            prev.move, 
                            prev.new_state, 
                            step.move, 
                            step.new_state)

        yield MDPStep(prev_state = prev.prev_state, 
                      move = prev.move,
                      post_opp_move_state = step.new_state,
                      player = prev.player,
                      reward = reward)
        prev = step

    final_reward = mdp.reward(prev.prev_state, 
                              prev.move, 
                              prev.new_state)
    
    yield MDPStep(prev_state = prev.prev_state, 
                  move = prev.move,
                  post_opp_move_state = prev.new_state.response(),
                  player = prev.player,
                  reward = final_reward)


if __name__ == '__main__':
    import tictactoe as rules
    import agent
    from mdp import MDP


    # TODO: This is duplicated from train.py -- find a good place for it!
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
    ## END TODO


    class HumanConsolePlayer:
        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return self.name

        def __str__(self):
            return self.__repr__()

        def move(self, curr_state):
            print('The current state is: \n' + str(curr_state))
            raw_move = input('Please input row and column separated by a space: ')
            row, col = raw_move.split(' ')
            row, col = int(row), int(col)
            return (row, col)


    mdp = MDP(rules)

    game = transitions(mdp, 
                   (HumanConsolePlayer("X's"), HumanConsolePlayer("O's")))
    game = transitions(mdp, 
                   (HumanConsolePlayer("X's"), 
                    TestingWrapper(agent.QLearner.load('champion.p'))))
    
    for step in game:
        print(str(step.player) + " earns " + str(step.reward) + " points!")
        
    print(step.post_opp_move_state)
