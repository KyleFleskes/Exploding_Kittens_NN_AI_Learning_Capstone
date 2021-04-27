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

from Neural_Networked_Tree.Game.Exploding_Kittens import Game as ek
from Neural_Networked_Tree.Game.Gamestate import ExplodingKittensAbstractGameState as gs

from Neural_Networked_Tree.Tree.MonteCarloTreeSearchNode import TwoPlayersGameMonteCarloTreeSearchNode as NNnode
from Vanilia_Tree.Tree.MonteCarloTreeSearchNode import TwoPlayersGameMonteCarloTreeSearchNode as Vnode
from Neural_Networked_Tree.Tree.MonteCarloTreeSearch import MonteCarloTreeSearch as NNtree
from Vanilia_Tree.Tree.MonteCarloTreeSearch import MonteCarloTreeSearch as Vtree
board_state = gs()

# Disable


def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore


def enablePrint():
    sys.stdout = sys.__stdout__


def updateScreen():
    if board_state.game.currentPlayer == 0:  # oppenent == 1, player == 0
        print("---------------------------------------------------------------------")
        if board_state.game.currentPlayer:  # oppenent == 1, player == 0
            cprint("  It is your oppenent's turn", "red")
        else:
            print("  It is your turn")
        print("")

        print("  Number of cards in draw pile: " +
              str(len(board_state.game.drawingPile)))
        print("  Number of cards in oppenents hand: " +
              str(len(board_state.game.player[1].cards)))
        print("  Number cards revealed by see the future by oppenent: " +
              str(len(board_state.game.knownCards1)))
        print("")

        stfString = ""
        for card in board_state.game.knownCards0:
            stfString += "["+card.type+"] "
        print("  See the future cards: " +
              stfString)
        handString = ""
        for card in board_state.game.player[0].cards:
            handString += "["+card.type+"] "
        print("  Your hand: " +
              handString + "|| {draw}")
        print("")
        print("---------------------------------------------------------------------")

    else:
        cprint("---------------------------------------------------------------------")
        if board_state.game.currentPlayer:  # oppenent == 1, player == 0
            cprint("  It is your oppenent's turn", "red")
        else:
            cprint("  It is your turn", "red")
        cprint("")

        cprint("  Number of cards in draw pile: " +
               str(len(board_state.game.drawingPile)), "red")
        cprint("  Number of cards in oppenents hand: " +
               str(len(board_state.game.player[1].cards)), "red")
        cprint("  Number cards revealed by see the future by oppenent: " +
               str(len(board_state.game.knownCards1)), "red")
        cprint("")

        cprint("")
        cprint(
            "---------------------------------------------------------------------", "red")


def printGameOver(screen):
    if board_state.game.currentPlayer == 0:
        effects = [
            Cycle(
                screen,
                FigletText("EXPLODING  KITTEN!!!", font='big'),
                screen.height // 2 - 8),
            Cycle(
                screen,
                FigletText("YOU LOST!", font='big'),
                screen.height // 2 + 3),
            Stars(screen, (screen.width + screen.height) // 2),
            # ExplosionFlames(screen, screen.width // 2, screen.height // 2, 5)
            # screen.print_at("(Enter CRTL+C to exit...)", 0, 0)
        ]
        screen.play([Scene(effects, 500)])
    else:
        effects = [
            Cycle(
                screen,
                FigletText("EXPLODING  KITTEN!!!", font='big'),
                screen.height // 2 - 8),
            Cycle(
                screen,
                FigletText("YOU WON!", font='big'),
                screen.height // 2 + 3),
            Stars(screen, (screen.width + screen.height) // 2),
            # ExplosionFlames(screen, screen.width // 2, screen.height // 2, 5)
            # screen.print_at("(Enter CRTL+C to exit...)", 0, 0)
        ]

    screen.play([Scene(effects, 500)])


print("-------             Welcome to our Capstone project!           -------")
print("Please follow the prompts to play a game of Exploding Kittens against our AI")
print('')
opponent = input(
    'Would you like to play against our vanilla AI or our neural network AI? [V, NN] ')
move_count = int(input('How difficult would the AI to be? [0-100] ')) + 1
print('Thank you for playing, enjoy your game!')
sleep(2)

print("                                                                     ")
print("                             Game is Starting                        ")
print("                                                                     ")
while not board_state.is_game_over():
    updateScreen()
    # This is the gameloop for the player
    while board_state.game.currentPlayer == 0:
        choice = input("Select a card to play by name or draw:")
        while(not board_state.game.player[board_state.game.currentPlayer].playTurn(choice)):
            choice = input("Select a card to play by name or draw:")
        updateScreen()

        if not board_state.is_game_over() and board_state.game.explosionStatus:
            choice = input("Play your defuse card!!!")
            while(not board_state.game.player[board_state.game.currentPlayer].playTurn(choice)):
                choice = input("PLAY YOUR DEFUSE CARD!!!")

    # this is the gameloop for the ai
    while board_state.game.currentPlayer == 1:
        if board_state.is_game_over():
            break

        if opponent == 'V':
            root = Vnode(board_state)
            t = Vtree(root)
            blockPrint()
            action = t.best_action(move_count)
            enablePrint()
            board_state = board_state.move(action)
            # enablePrint()

        elif opponent == 'NN':
            root = NNnode(board_state)
            t = NNtree(
                root, 'C:/Users/digit/OneDrive/Documents/GitHub/Reinforcement_Learning_Capstone-2/Neural_Networked_Tree/Models/Exploding_Cat_Model-1000.h5')
            blockPrint()
            action = t.best_action(move_count)
            enablePrint()
            board_state = board_state.move(action)
            # enablePrint()

        elif opponent == 'random':
            blockPrint()
            board_state = board_state.move(random.choice(
                board_state.get_legal_actions()))
            enablePrint()

Screen.wrapper(printGameOver)
