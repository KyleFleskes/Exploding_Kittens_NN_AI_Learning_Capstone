# This is a modified version of the online available Monte Carlo Search Tree
# at https://github.com/int8/monte-carlo-tree-search
# This has been changed and commented to increase readablity while also changing some functions
# to fit Exploding Kittens rather than Tic Tac Toe.
import numpy as np
import random

from Tree.MonteCarloTreeSearchNode import TwoPlayersGameMonteCarloTreeSearchNode as node
from Tree.MonteCarloTreeSearch import MonteCarloTreeSearch as tree
from Game.Gamestate import ExplodingKittensAbstractGameState as gs
#from TicTacToe import TicTacToeGameState

# Does a pretty print of the search tree.


def pprint_tree(node, file=None, _prefix="", _last=True):
    print(_prefix, "`- " if _last else "|- ",
          node.state.board, sep="", file=file)
    _prefix += "   " if _last else "|  "
    child_count = len(node.children)
    for i, child in enumerate(node.children):
        _last = i == (child_count - 1)
        pprint_tree(child, file, _prefix, _last)

# Takes in a card type i.e. attack, defuse, rainbow etc. and returns its index in the indexToType dictionary.


def typeToIndex(indexToChoice, Type):
    index = None

    for key, value in indexToChoice.items():
        # if the value is in the dictionary
        if Type == value:
            index = key

    return index


# This is the driver code to get TicTacToe,
# note somechanges need to be made in MonteCarloTreeSearchNode to make this work.
'''
state = np.zeros((3,3))

initial_board_state = TicTacToeGameState(state = state, next_to_move=1)
#print(initial_board_state.board)
root = node(state = initial_board_state)
mcts = tree(root)
best_node = mcts.best_action(2)

#print(best_node.state.board)
pprint_tree(root)
'''

# This is some testing code to make sure the that
# get_obsersavtion_space(), get_legal_actions(), and move() works as intended in Gamestate.py
'''
board_state = gs()

print(board_state.get_obsersavtion_space())
print()
legal_actions = board_state.get_legal_actions()
print(legal_actions)
choice = random.choice(legal_actions)
print(choice)
index = typeToIndex(board_state.indexToChoice, choice)
print(index)

board_state = board_state.move(index)

print(board_state.get_obsersavtion_space())
print()
legal_actions = board_state.get_legal_actions()
print(legal_actions)
choice = random.choice(legal_actions)
print(choice)
index = typeToIndex(board_state.indexToChoice, choice)
print(index)
'''

board_state = gs()
print(board_state.is_game_over())
while (not board_state.is_game_over()):
    print(board_state.get_obsersavtion_space())
    # get list of legal actions based on gamestate.
    legal_actions = board_state.get_legal_actions()
    print(legal_actions)
    # if there are no vaild cards to play in your hand, draw a card and end your turn.
    if legal_actions is None:
        print("no legal actions, drawing a card and ending turn.")
        choice = 13
    # if there are cards to play in your hand, pick one legal action at random.
    else:
        choice = random.choice(legal_actions)  # pick a legal action at random.
    print(choice)
    # turn that legal action into an index of the observation space.
    index = typeToIndex(board_state.indexToChoice, choice)
    print(index)
    # update the board state based on action taken.
    board_state = board_state.move(index)

winner = board_state.game_result()
print("Player: ", winner, " is the winner!")
