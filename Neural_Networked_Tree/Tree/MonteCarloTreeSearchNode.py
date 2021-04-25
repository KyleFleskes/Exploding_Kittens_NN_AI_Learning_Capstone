# This is a modified version of the online available Monte Carlo Search Tree
# at https://github.com/int8/monte-carlo-tree-search
# This has been changed and commented to increase readablity while also changing some functions
# to fit Exploding Kittens rather than Tic Tac Toe.

import numpy as np
from collections import defaultdict
from abc import ABC, abstractmethod

# This is an abstract class that outlines the functions in a node of the MonteCarloTreeSearch.


class MonteCarloTreeSearchNode(ABC):

    # Create a node with given game state and a parent(by default having no parent) and no children.
    def __init__(self, state, parent=None):
        """
        Parameters
        ----------
        state : mctspy.games.common.TwoPlayersAbstractGameState
        parent : MonteCarloTreeSearchNode
        """
        self.state = state
        self.parent = parent
        self.children = []

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
        

    # An abstract method that will give the list of untried actions.
    @property
    @abstractmethod
    def untried_actions(self):
        """
        Returns
        -------
        list of mctspy.games.common.AbstractGameAction
        """
        pass

    # An abstract method that will give the q value of the node.
    @property
    @abstractmethod
    def q(self):
        pass

    # An abstract method that will give the number of times the current node was visited.
    @property
    @abstractmethod
    def n(self):
        pass

    # An abstract method that will pick an untried action for the given node
    # and simulate it, then add the new state to the tree.
    @abstractmethod
    def expand(self):
        pass

    # An abstract method that will return True if the current state is a game ending state.
    @abstractmethod
    def is_terminal_node(self):
        pass

    # An abstract method that will take in the current game state and simuates the game
    # with random action until a win or loss.
    @abstractmethod
    def rollout(self):
        pass

    # An abstract method that will take in if a simulated game result
    # and updates the whole tree accordingly.
    @abstractmethod
    def backpropagate(self, reward):
        pass

    # A method that checks if the current node has tried all avaible actions.
    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    # A method that uses the
    def best_child(self, c_param=1.4):
        choices_weights = [
            (c.q / c.n) + c_param * np.sqrt((2 * np.log(self.n) / c.n))
            for c in self.children
        ]
        #print(np.argmax(choices_weights))
        return self.children[np.argmax(choices_weights)]
    
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Change rollout policy to pick what the NN thinks is the best 
    # action based off of the observation space instead of just picking
    # a random choice.
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # picks a random action from the list of legal available actions.
    def rollout_policy(self, obs_space, possible_moves, model):
        
        # format ovsersavtion space of current node
        state = np.array(obs_space)
        state = state.reshape(-1,15)

        # use NN to make predictions of win rates for all moves moves.
        predictions = model.predict(state)
        predictions = predictions[0] # turn predictions into 1d array.
        
        # we add + 1 the indexTochoice because there are 14 card types but we never want to play the
        # 0th card type. This is ok because the NN outputs for 13 card types.
        valid_move = False
        best = np.argmax(predictions)
        choice = self.indexToChoice[best + 1]
        print(obs_space)
        print(possible_moves)
        # loop until choosen the best move that is valid.
        while(not valid_move):
            
            print(choice)
            # check if 'best' choice is in list of possible moves.
            if choice in possible_moves:
                valid_move = True
            # choice is not list of possible moves, then check next best.
            else:
                predictions[best] = 0
                best = np.argmax(predictions)
                choice = self.indexToChoice[best + 1]

        return choice

# This class represents an individual node in the Monte Carlo Search Tree.
class TwoPlayersGameMonteCarloTreeSearchNode(MonteCarloTreeSearchNode):

    def __init__(self, state, parent=None, action=None):
        super().__init__(state, parent)
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._untried_actions = None
        self.wins = 0
        self.loses = 0
        self.action = action

    @property
    def untried_actions(self):
        if self._untried_actions is None:
            self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    @property
    def q(self):
        # changed to use game.currentplayer
        if self.parent is not None:
            
            self.wins = self._results[self.parent.state.game.currentPlayer]
            self.loses = self._results[abs(self.parent.state.game.currentPlayer - 1)]
            
            #wins = self._results[self.parent.state.next_to_move]
            #loses = self._results[-1 * self.parent.state.next_to_move]
        return self.wins - self.loses

    @property
    def n(self):
        return self._number_of_visits

    # picks an untried action for the current node and simulates it,
    # then adds the state to the tree. Returns the newly created node.
    def expand(self):
        # pick an untried action
        action = self.untried_actions.pop()
        # simulate the action
        next_state = self.state.move(action)
        # add the new games state to the tree as a child of the current node.
        child_node = TwoPlayersGameMonteCarloTreeSearchNode(next_state, parent=self, action=action)
        self.children.append(child_node)
        return child_node

    # This method returns True if the current state is a game ending state.
    def is_terminal_node(self):
        return self.state.is_game_over()

    # this takes in the current game state and simuates the game with
    # random action until a win or loss.
    def rollout(self, model):
        current_rollout_state = self.state
        
        # while current state is not a game ending state.
        while not current_rollout_state.is_game_over():
            # get a list of legal actions based on the game state.
            possible_moves = current_rollout_state.get_legal_actions()
            # pick a random move from available actions.
            action = self.rollout_policy(current_rollout_state.get_obsersavtion_space(), possible_moves, model)
            # take the action, and make the new game state the current one.
            current_rollout_state = current_rollout_state.move(action)
        #print("Game result: ", current_rollout_state.game_result())

        return current_rollout_state.game_result()

    # this method takes in if a simulated game result
    # and updates the whole tree accordingly.
    def backpropagate(self, result):
        #print(self.state.get_obsersavtion_space())
        self._number_of_visits += 1
        
        if len(self._results) == 0:
            self._results[0] = 0
            self._results[1] = 0
        # keep track of if the nodes children resulted in a win or a loss.
        self._results[result] += 1
        #print(self._results)
        # if not the root of the tree, go to current node's parent.
        if self.parent:
            self.parent.backpropagate(result)
