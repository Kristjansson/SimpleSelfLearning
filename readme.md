# Self Learning for Simple Games

This is a small project exploring systems that self learn to play simple games. This is inspired by Deepmind's AlphaGo, but aimed at Tic Tac Toe and Checkers. Hopefully this will keep the systems simple so that the code can be concise, and they can be trained on hardware available to mere mortals. 

## Todo Items

  1. ~~Code seems to be working well, but agent performance vs human is poor.
  ..+ Investigate adding penalities to losers. Currently code is designed so that only agent who last moved can recieve a reward/penalty, so this will require some refactoring.~~
  train.py produces an agent that seems to play optimally when manually testing.

  2. Implement unit tests
  3. Implement a minimax/ provably optimal agent to benchmark RL agent against
  4. Implement a checkers ruleset
  5. Tackle the larger state space.
