"""A reusable framework for iterating through games"""

from collections import namedtuple

MDPStep = namedtuple('MDPStep', ['prev_state', 'move', 'new_state', 'player', 'reward'])

def episode(mdp, players):
    curr_state = mdp.initial_state()
    while not curr_state.game_over():
        curr_player = players[0]
        move = curr_player.move(curr_state)
        new_state = curr_state.move(move)
        reward = mdp.reward(curr_state, move, new_state)
            
        yield MDPStep(prev_state = curr_state, 
                      move = move,
                      new_state = new_state,
                      player = curr_player,
                      reward = reward)

        curr_state = new_state
        players = (*players[1:], players[0])



if __name__ == '__main__':
    import tictactoe
    import agent


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
        def move(self, curr_state):
            print('The current state is: \n' + str(curr_state))
            raw_move = input('Please input row and column separated by a space: ')
            row, col = raw_move.split(' ')
            row, col = int(row), int(col)
            return (row, col)



    game = episode(tictactoe.TicTacToe_MDP(), 
                   (HumanConsolePlayer(), TestingWrapper(agent.QLearner.load('champion.p'))))
    
    for step in game:
        pass
    print(step.new_state)

    input('Thanks for playing, press Enter to close!')