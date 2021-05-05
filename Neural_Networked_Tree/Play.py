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

from Tree.MonteCarloTreeSearchNode import TwoPlayersGameMonteCarloTreeSearchNode as node
from Tree.MonteCarloTreeSearch import MonteCarloTreeSearch as tree
from Game.Gamestate import ExplodingKittensAbstractGameState as gs

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
        expStat = board_state.game.explosionStatus
        root = node(board_state)
        t = tree(root, 'C:/Users/flesk/Desktop/qlearning/Git Exploding Kittens/Reinforcement_Learning_Capstone/Neural_Networked_Tree/Models/Exploding_Cat_Model-big.h5')
        blockPrint()
        action = t.best_action(5)
        enablePrint()
        board_state = board_state.move(action)

Screen.wrapper(printGameOver)
