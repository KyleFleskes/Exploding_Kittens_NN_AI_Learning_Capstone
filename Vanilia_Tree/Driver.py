# This is a modified version of the online available Monte Carlo Search Tree
# at https://github.com/int8/monte-carlo-tree-search
# This has been changed and commented to increase readablity while also changing some functions
# to fit Exploding Kittens rather than Tic Tac Toe.
import numpy as np

from Tree.MonteCarloTreeSearchNode import TwoPlayersGameMonteCarloTreeSearchNode as node
from Tree.MonteCarloTreeSearch import MonteCarloTreeSearch as tree
from Game.Gamestate import ExplodingKittensAbstractGameState as gs

# Does a pretty print of the search tree.
def pprint_tree(node, file=None, _prefix="", _last=True):
    print(_prefix, "`- " if _last else "|- ", "P:",node.state.game.currentPlayer, " ",
          node.state.get_obsersavtion_space(), "#'s visited: ", node.n, " #'s wins: ", node._results[0], " #'s loses: ", node._results[1], sep="", file=file)
    _prefix += "   " if _last else "|  "
    child_count = len(node.children)
    for i, child in enumerate(node.children):
        _last = i == (child_count - 1)
        pprint_tree(child, file, _prefix, _last)




board_state = gs()
root = node(board_state)
t = tree(root)
action = t.best_action(1000)

pprint_tree(root)
print("Best next move: ", action)

'''
board_state = gs()

while not board_state.is_game_over():
    root = node(board_state)
    t = tree(root)
    action = t.best_action(50)
    board_state = board_state.move(action)
'''