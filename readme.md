# Self Learning for Simple Games

This is a small project exploring systems that self learn to play simple games. This is inspired by Deepmind's AlphaGo, but aimed at Tic Tac Toe and Checkers. Hopefully this will keep the systems simple so that the code can be concise, and they can be trained on hardware available to mere mortals. 

## Running
To use this library, simply clone the repository then execute either train.py or game.py. 
1. The train.py file trains agents from scratch and saves the best agent it finds in a file called champion.p. 
2. The game.py file allows a human to play against this agent on the console. User moves are specified by specifying the row and col number separated by a space, i.e. 0 1 [ENTER] to play in the top middle space. 


## Todo Items

  1. ~~Code seems to be working well, but agent performance vs human is poor.
  ..+ Investigate adding penalities to losers. Currently code is designed so that only agent who last moved can recieve a reward/penalty, so this will require some refactoring.~~
  train.py produces an agent that seems to play optimally when manually testing.

  2. Implement unit tests
  3. ~~Implement a minimax/ provably optimal agent~~ to benchmark RL agent against
  4. Implement a checkers ruleset
  5. Tackle the larger state space.
