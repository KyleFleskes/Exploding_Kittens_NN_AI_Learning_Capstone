## Reinforcement_Learning_Capstone : python implementation of Monte Carlo Tree Search algorithm for Exploding Kittens.

 
Basic python implementation of [Monte Carlo Tree Search](https://int8.io/monte-carlo-tree-search-beginners-guide) (MCTS) intended to run the card game Exploding Kittens. 
 

### Installation

1. Download either the Vanilia_Tree folder or the NN_Tree folder. The Vanilia_Tree contains a monte carlo search tree(MCST) that simulates the card game Exploding Kittens.
   The NN_Tree contains a MCST that takes advangate of a neural network(NN).
   WARNING: You need to have your gpu configured for tensorflow to work. See guide: [Tensorflow GPU](https://www.tensorflow.org/install/gpu)
2. Import the chosen folder into your python IDE of your choice.
3. Use or create a driver file in either /.../Vanilia_Tree/ or /.../NN_Tree/ and use the example code below to have the AI decide it's next action based off the gamestate.

### Running Exploding Kitten example 

to run Exploding Kittens example:

```python
import numpy as np


from Tree.MonteCarloTreeSearchNode import TwoPlayersGameMonteCarloTreeSearchNode as node
from Tree.MonteCarloTreeSearch import MonteCarloTreeSearch as tree
from Game.Gamestate import ExplodingKittensAbstractGameState as gs

board_state = gs()
root = node(board_state)
t = tree(root)
action = t.best_action(1000)

pprint_tree(root)
print("Best next move: ", action)

```
