# This is a modified version of the online available Monte Carlo Search Tree
# at https://github.com/int8/monte-carlo-tree-search
# This has been changed and commented to increase readablity while also changing some functions
# to fit Exploding Kittens rather than Tic Tac Toe.
from abc import ABC, abstractmethod
try:
    from Exploding_Kittens import Game as game
except ImportError:
    from .Exploding_Kittens import Game as game
import copy


# This is an abstract class for a given two player game.
class TwoPlayersAbstractGameState(ABC):

    # An abstract method that determines which if any player has won or lost.
    @abstractmethod
    def game_result(self):
        """
        this property should return:
         1 if player #1 wins
        -1 if player #2 wins
         0 if there is a draw
         None if result is unknown
        Returns
        -------
        int
        """
        pass

    # An abstract method that determines if the current game state is a game ending state.
    @abstractmethod
    def is_game_over(self):
        """
        boolean indicating if the game is over,
        simplest implementation may just be
        `return self.game_result() is not None`
        Returns
        -------
        boolean
        """
        pass

    # An abstract method that takes in an action(an index) and returns the resultant gamestate.
    @abstractmethod
    def move(self, action):
        """
        consumes action and returns resulting TwoPlayersAbstractGameState
        Parameters
        ----------
        action: AbstractGameAction
        Returns
        -------
        TwoPlayersAbstractGameState
        """
        pass

    # An abstract method that returns the list of all legal actions of the current game state.
    @abstractmethod
    def get_legal_actions(self):
        """
        returns list of legal action at current game state
        Returns
        -------
        list of AbstractGameAction
        """
        pass

# An abstract class that represents an action that can be taken.


class AbstractGameAction(ABC):
    pass


# This class represents the game state of Exploding Kittens
class ExplodingKittensAbstractGameState(ABC):

    def __init__(self, previousGame=None, make_data=False):
        if not previousGame:
            self.game = game()
            if (make_data):
                self.game.start_reduced_Game()
            else:
                self.game.startGame()
            # self.game = game.Game() # note im having trouble with this.
        else:
            self.game = previousGame
        # game.drawingPile = []
        # game.playedCards = []
        # game.currentPlayer = 0
        # game.isGameOver = False
        # game.noOfTurn = 0
        # game.explosionStatus = False
        # game.knownCards = []
        # game.moves = []
        # game.player = []

        self.indexToChoice = {
            0: 'kitten',  # likely should be removed
            1: 'attack',
            2: 'skip',
            3: 'favor',
            4: 'shuffle',
            5: 'see-the-future',
            6: 'draw-from-bottom',
            7: 'defuse',
            8: 'taco',
            9: 'watermelon',
            10: 'potato',
            11: 'beard',
            12: 'rainbow',
            13: 'draw'
        }

    # A method that determines which if any player has won or lost.
    def game_result(self):
        """
        this property should return:
         0 if player #0 wins
         1 if player #1 wins
         None if result is unknown
        Returns
        -------
        int
        """
        if self.game.isGameOver:
            if self.game.currentPlayer == 0:
                return 1
            else:
                return 0
        else:
            return None

    # A method that determines if the current game state is a game ending state.
    def is_game_over(self):
        """
        boolean indicating if the game is over,
        simplest implementation may just be
        `return self.game_result() is not None`
        Returns
        -------
        boolean
        """
        return self.game.isGameOver  # note I changed this to checkGameOver from is_game_over.

    # A method that takes in an action(an index) and returns the resultant gamestate.
    def move(self, action):
        """
        consumes action and returns resulting TwoPlayersAbstractGameState
        Parameters
        ----------
        action: AbstractGameAction
        Returns
        -------
        TwoPlayersAbstractGameState
        """

        gameCopy = copy.deepcopy(self.game)

        if isinstance(action, str):
            gameCopy.player[gameCopy.currentPlayer].playTurn(action)
        elif isinstance(action, int):
            gameCopy.player[gameCopy.currentPlayer].playTurn(
                self.indexToChoice[action])
        else:
            print("Invalid argument in gamestate.move")
        # print(self.game.moves)
        # print(gameCopy.moves)

        return ExplodingKittensAbstractGameState(gameCopy)

    # A method that returns the list of all legal actions of the current game state.
    def get_legal_actions(self):
        """
        returns list of legal action at current game state
        Returns
        -------
        list of AbstractGameAction
        """
        legalActions = []
        for i in self.indexToChoice.values():
            if self.game.player[self.game.currentPlayer].testMove(i):
                legalActions.append(i)
        return legalActions

    # returns the action space for the AI to make decisions on.
    # note: this has been reworked by I(Kyle) because of bug fixing.
    def get_obsersavtion_space(self):
        hand = [0] * 13

        # for each card in the player's hand.
        for i in self.game.player[self.game.currentPlayer].cards:
            # search the indexToChoice of the card type.
            for key, value in self.indexToChoice.items():
                # if the value is in the dictionary
                if i.type == value:
                    hand[key] = hand[key] + 1

        #-1 means no previous card was played.
        lastPlayed = [-1]

        # if there is a last played card.
        if self.game.playedCards:
            # look for card type index inside of indexToChoice.
            for key, value in self.indexToChoice.items():
                # if found card type.
                if self.game.playedCards[0].type == value:
                    # print(value)
                    lastPlayed[0] = key

        cardsInDeck = [len(self.game.drawingPile)]

        obv_space = hand + lastPlayed + cardsInDeck
        return obv_space
