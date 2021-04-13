# This is a modified version of the online available Monte Carlo Search Tree
# at https://github.com/int8/monte-carlo-tree-search
# This has been changed and commented to increase readablity while also changing some functions
# to fit Exploding Kittens rather than Tic Tac Toe.
import numpy as np
import random

from Tree.MonteCarloTreeSearchNode import TwoPlayersGameMonteCarloTreeSearchNode as node
from Tree.MonteCarloTreeSearch import MonteCarloTreeSearch as tree
from Game.Gamestate import ExplodingKittensAbstractGameState as gs
# from TicTacToe import TicTacToeGameState

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


# This is some testing code to make sure that
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
# This is some test code to make sure that
# is_game_over(), and game_result() works as intended.
'''
board_state = gs()
print(board_state.is_game_over())
while (not board_state.is_game_over()):
    print(board_state.get_obsersavtion_space())
    # get list of legal actions based on gamestate.
    legal_actions = board_state.get_legal_actions()
    print(legal_actions)
    # if there are no vaild cards to play in your hand, draw a card and end your turn.
    
    choice = random.choice(legal_actions)  # pick a legal action at random.
    print(choice)
    # turn that legal action into an index of the observation space.
    index = typeToIndex(board_state.indexToChoice, choice)
    print(index)
    # update the board state based on action taken.
    board_state = board_state.move(index)

winner = board_state.game_result()
print("Player: ", winner, " is the winner!")
'''

board_state = gs()  # create the initial game baord state.
root = node(board_state)  # put that board state into a node.
# print(root.untried_actions)
# print(root.q)
# print(root.n)
while (not root.is_fully_expanded()):
    # print(root.state.get_obsersavtion_space())
    # print(root.untried_actions)
    root.expand()


# print(root.children)
'''
board_state = gs() # create the initial game baord state.
root = node(board_state) # put that board state into a node.
tree = tree(root) # put that node at the root of the tree.

tree.best_action(1)
'''
