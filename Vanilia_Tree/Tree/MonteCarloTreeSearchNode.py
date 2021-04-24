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
    
    # picks a random action from the list of legal available actions.
    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

# This class represents an individual node in the Monte Carlo Search Tree.
class TwoPlayersGameMonteCarloTreeSearchNode(MonteCarloTreeSearchNode):

    def __init__(self, state, parent=None, action=None):
        super().__init__(state, parent)
        self._number_of_visits = 0.
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
    def rollout(self, owner):
        current_rollout_state = self.state
        # while current state is not a game ending state.
        while not current_rollout_state.is_game_over():
            # get a list of legal actions based on the game state.
            possible_moves = current_rollout_state.get_legal_actions()
            # pick a random move from available actions.
            action = self.rollout_policy(possible_moves)
            # take the action, and make the new game state the current one.
            current_rollout_state = current_rollout_state.move(action)
        print("Game result: ", current_rollout_state.game_result(owner))
        return current_rollout_state.game_result(owner)

    # this method takes in if a simulated game result
    # and updates the whole tree accordingly.
    def backpropagate(self, result):
        #print("Game result: ", current_rollout_state.game_result())
        #print(self.state.get_obsersavtion_space())
        self._number_of_visits += 1.
        # keep track of if the nodes children resulted in a win or a loss.
        self._results[result] += 1.
        # if not the root of the tree, go to current node's parent.
        if self.parent:
            self.parent.backpropagate(result)
