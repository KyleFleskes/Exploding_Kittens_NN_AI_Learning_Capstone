import Game.Exploding_Kittens as ek
import random
#from asciimatics.screen import Screen
#from asciimatics.scene import Scene
#from asciimatics.effects import Cycle, Stars
#from asciimatics.renderers import FigletText
#from asciimatics.particles import ExplosionFlames, Explosion, StarExplosion
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
p0_search = 1
p1_search = 1
iterations = 100  # https://en.wikipedia.org/wiki/Checking_whether_a_coin_is_fair
opponent = 'random'
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
            # enablePrint()
            board_state = board_state.move(action)
            enablePrint()

        while board_state.game.currentPlayer == 1:
            if board_state.is_game_over():
                break
            if opponent == 'AI':
                root = node(board_state)
                t = tree(root)
                blockPrint()
                action = t.best_action(p1_search)
                # enablePrint()
                board_state = board_state.move(action)
                enablePrint()
            elif opponent == 'random':
                blockPrint()
                board_state = board_state.move(random.choice(
                    board_state.get_legal_actions()))
                enablePrint()
            else:
                print('please choose AI or random')

    # print('winner', board_state.game_result())
    winsLosses.append(board_state.game_result())

# print(winsLosses)
entry = {
    'p0_search': p0_search,
    'p1_search': p1_search,
    'iterations': iterations,
    'wins': iterations - sum(winsLosses),
    'loss': sum(winsLosses),
    'ratio': (iterations - sum(winsLosses))/sum(winsLosses),
    'raw': str(winsLosses),
}

fname = 'wins&losses-'+str(iterations)+'-' + \
    str(p0_search)+'-'+str(p1_search) + '-vs-' + opponent + '.json'
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
