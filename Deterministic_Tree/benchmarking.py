import Game.Exploding_Kittens as ek
import random
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.effects import Cycle, Stars
from asciimatics.renderers import FigletText
from asciimatics.particles import ExplosionFlames, Explosion, StarExplosion
from time import sleep
import numpy as np
import random
import sys
import os
from termcolor import colored, cprint
import pickle
import json

from Tree.MonteCarloTreeSearchNode import TwoPlayersGameMonteCarloTreeSearchNode as node
from Tree.MonteCarloTreeSearch import MonteCarloTreeSearch as tree
from Game.Gamestate import ExplodingKittensAbstractGameState as gs


# Disable


def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore


def enablePrint():
    sys.stdout = sys.__stdout__


winsLosses = []
p0_search = 14
p1_search = 1
iterations = 100  # https://en.wikipedia.org/wiki/Checking_whether_a_coin_is_fair
for i in range(iterations):
    board_state = gs()
    print(i)
    while not board_state.is_game_over():

        while board_state.game.currentPlayer == 0:
            if board_state.is_game_over():
                break
            root = node(board_state)
            t = tree(root)
            blockPrint()
            action = t.best_action(p0_search)
            board_state = board_state.move(action)
            enablePrint()

        while board_state.game.currentPlayer == 1:
            if board_state.is_game_over():
                break
            root = node(board_state)
            t = tree(root)
            blockPrint()
            action = t.best_action(p1_search)
            board_state = board_state.move(action)
            enablePrint()
    winsLosses.append(board_state.game_result(0))

# print(winsLosses)
entry = {
    'p0_search': p0_search,
    'p1_search': p1_search,
    'iterations': iterations,
    'wins': sum(winsLosses),
    'loss': iterations - sum(winsLosses),
    'ratio': sum(winsLosses)/(iterations - sum(winsLosses)),
    'raw': str(winsLosses),
}

fname = 'wins&losses.json'
a = []
if not os.path.isfile(fname):
    a.append(entry)
    with open(fname, mode='w') as f:
        f.write(json.dumps(a, indent=2))
else:
    with open(fname) as feedsjson:
        feeds = json.load(feedsjson)

    feeds.append(entry)
    with open(fname, mode='w') as f:
        f.write(json.dumps(feeds, indent=2))
