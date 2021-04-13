import math
import random


# ----------------------------------------------------------------
#                           MAIN.py
# ----------------------------------------------------------------
checkPlayer = None


# def player1Timer():
# clearInterval(checkPlayer)
# checkPlayer = setInterval(lambda:
#                           if game.currentPlayer == 1:
#                           computerPlayer(), 6000)


def player1Draw(game):
    game.player[game.currentPlayer].drawCard(0)

# ----------------------------------------------------------------
#                           GAME.py
# ----------------------------------------------------------------


class Game ():
    def __init__(self):
        self.drawingPile = []
        self.playedCards = []
        self.currentPlayer = 0
        self.isGameOver = False
        self.noOfTurn = 0
        self.explosionStatus = False
        self.knownCards0 = []
        self.knownCards1 = []
        self.moves = []
        self.player = []

    def startGame(self):  # not sure if simply removing the new keyword is ok
        self.player.append(Player(self))
        self.player.append(Player(self))

        for i in range(4):
            #
            self.drawingPile.append(ShuffleCard(self))
            self.drawingPile.append(SkipCard(self))
            # self.drawingPile.append(SeeTheFutureCard(self))
            self.drawingPile.append(AttackCard(self))
            # self.drawingPile.append(DrawFromBottomCard(self))
            self.drawingPile.append(FavorCard(self))

            self.drawingPile.append(TacoCard(self))
            self.drawingPile.append(WatermelonCard(self))
            self.drawingPile.append(PotatoCard(self))
            self.drawingPile.append(BeardCard(self))
            self.drawingPile.append(RainbowCard(self))

        # There are 5 of these cards rather than 4
        # self.drawingPile.append(SeeTheFutureCard(self))
        # self.drawingPile.append(NopeCard(self))

        # insert 2 defuse unless there are more than 4 players
        for i in range(min(2, 6-len(self.player))):
            self.drawingPile.append(DefuseCard(self))
        self.shuffle()

        self.shuffle()

        # Deal each player their hand
        for i in range(len(self.player)):
            for j in range(7):
                self.player[i].cards.append(self.drawingPile[j])
                self.drawingPile.pop(0)
            self.player[i].cards.append(DefuseCard(self))

        # Insert the exploding kittens
        for i in range(len(self.player) - 1):
            self.drawingPile.append(ExplodingKittenCard(self))
        self.shuffle()
        # print(self)
        # player1Timer()

    def shuffle(self):
        i = len(self.drawingPile) - 1
        while i > 0:
            num = math.floor(random.random() *
                             (len(self.drawingPile)-1))  # maybe
            temp = self.drawingPile[i]
            self.drawingPile[i] = self.drawingPile[num]
            self.drawingPile[num] = temp
            i -= 1

    def checkGameOver(self):
        # if current player hand is empty?????
        if len(self.player[self.currentPlayer].cards) == 0:
            self.isGameOver = True
        return self.isGameOver

    # this is a method I added for method in Gamestate.py for the same name.
    def is_game_over(self):
        return self.explosionStatus

    def whoWon(self):
        print('start')
        return 1 - self.currentPlayer

    def switchPlayer(self):
        if self.currentPlayer == 1:
            self.currentPlayer = 0
            # showYourTurn()
        else:
            self.currentPlayer = 1

    def restart(self):
        self.drawingPile = []
        self.playedCards = []
        self.currentPlayer = 0
        self.isGameOver = False
        self.noOfTurn = 0
        self.explosionStatus = False
        self.knownCards0 = []
        self.knownCards1 = []
        self.moves = []
        self.player = []
        # print('before', self)
        self.startGame()
        # updateNotice()
        # updateDisplay()
        # print(self)

    def checkTurns(self):
        if self.noOfTurn == 0:
            self.switchPlayer()
        else:
            self.noOfTurn -= 1

    # def insertKitten(self, indec):  # typo?
    #     temp = self.drawingPile[0]

    #     if index >= 0 and index <= 2:
    #         self.drawingPile.pop(0)
    #         self.drawingPile.splice(index, 0, temp)
    #     elif index == 3:
    #         self.drawingPile.pop(0)
    #         self.drawingPile.append(temp)
    #     elif index == 4:
    #         self.shuffle()
    #     self.checkTurns()

    def insertKitten(self, index):
        temp = self.drawingPile[0]
        if isinstance(temp, ExplodingKittenCard):
            self.drawingPile.pop(0)
            self.drawingPile.insert(index, temp)
        else:
            # This case of for draw from bottom
            temp = self.drawingPile.pop()
            self.drawingPile.insert(index, temp)

        # if index >= 0 and index <= 2:
        #     self.drawingPile.pop(0)
        #     self.drawingPile.insert(index, temp)
        # elif index == 3:
        #     self.drawingPile.pop(0)
        #     self.drawingPile.append(temp)
        # elif index == 4:
        #     self.shuffle()
        # self.checkTurns()

    def stealRandom(self):
        if len(self.player) == 2:
            target = abs(self.currentPlayer - 1)
            if self.player[target].cards != []:
                index = random.randint(0, len(self.player[target].cards)-1)
                card = self.player[target].cards.pop(index)
                self.player[self.currentPlayer].cards.append(card)
                print(card.type + " was stolen!")
        else:
            print("THIS FUNCTION CAN ONLY HANDLE 2 PLAYERS")
# ----------------------------------------------------------------
#                           PLAYER.py
# ----------------------------------------------------------------


class Player(object):

    def __init__(self, game):
        self.game = game
        self.cards = []
        self.moves = []
        self.cardDict = {
            'kitten': 0,
            'attack': 0,
            'skip': 0,
            'favor': 0,
            'shuffle': 0,
            'see-the-future': 0,
            'draw-from-bottom': 0,
            'defuse': 0,
            'taco': 0,
            'watermelon': 0,
            'potato': 0,
            'beard': 0,
            'rainbow': 0,
        }

    def playTurn(self, choice):
        expStat = self.game.explosionStatus
        if (self.game.explosionStatus is True) and not any(isinstance(i, DefuseCard) for i in self.game.player[self.game.currentPlayer].cards):
            self.game.isGameOver = True
            return False

        if choice == "draw":
            self.drawCard(0)
            return True
        if choice not in self.cardDict.keys():
            print("Invalid choice.")
            return False
        currHand = self.cardDict.copy()
        choiceIndexes = []
        for i, card in enumerate(self.cards):
            currHand[card.type] += 1
            if card.type == choice:
                choiceIndexes.append(i)

        if self.game.isGameOver is False:
            if self.game.explosionStatus is True:
                if choice != 'defuse':
                    print('Player ' + str(self.game.currentPlayer)+': ' + 'cannot play ' +
                          choice + ' while an explosion is active!')
                    return False
            else:
                if choice == 'defuse':
                    print('Player ' + str(self.game.currentPlayer)+': ' + 'cannot play ' +
                          choice + ' while an explosion is not active!')
                    return False

            if choice in ['taco', 'watermelon', 'potato', 'beard', 'rainbow']:
                if currHand[choice] < 2:
                    print('there are not enough '+choice+'s in your hand')
                    return False

                print('Player ' + str(self.game.currentPlayer) +
                      ': played ' + choice + ' pair')
                self.cards.pop(choiceIndexes.pop())

            if currHand[choice] < 1:
                print(choice + ' is not in your hand')
                return False
            print('Player ' + str(self.game.currentPlayer) +
                  ': played ' + choice)

            self.game.playedCards.insert(0, self.cards[choiceIndexes[0]])
            self.moves.insert(0, self.cards[choiceIndexes[0]].type)
            temp = {}
            temp[self.game.currentPlayer] = self.cards[choiceIndexes[0]].type
            self.game.moves.insert(0, temp)
            self.cards.pop(choiceIndexes[0])  # self.cards.splice(choice, 1)
            self.game.playedCards[0].render()

            # This segment should be reformatted.
            if expStat != self.game.explosionStatus:
                if self.game.currentPlayer == -999:  # Temporarily set to -999 so it is always random
                    index = -1
                    while not (index >= 0 and index <= len(self.game.drawingPile)-1):
                        # this doesn't handle invlaid inputs
                        index = int(input("Please select an index between 0 and {x} where 0 is the top of the deck and {x} is the bottom ".format(
                            x=len(self.game.drawingPile)-1)))
                    self.game.insertKitten(index)
                else:
                    self.game.insertKitten(random.randint(
                        0, len(self.game.drawingPile)-1))

            return True
        else:
            return False

    # note I(Kyle) commented out the prints in this function for testing purposes.
    def testMove(self, choice):
        if choice == "draw":
            return True
        if choice not in self.cardDict.keys():
            #print("Invalid choice.")
            return False
        currHand = self.cardDict.copy()
        choiceIndexes = []
        for i, card in enumerate(self.cards):
            currHand[card.type] += 1
            if card.type == choice:
                choiceIndexes.append(i)

        if self.game.isGameOver is False:
            if self.game.explosionStatus is True:
                if choice != 'defuse':
                    # print('Player ' + str(self.game.currentPlayer)+': ' + 'cannot play ' +
                    # choice + ' while an explosion is active!')
                    return False
            else:
                if choice == 'defuse':
                    # print('Player ' + str(self.game.currentPlayer)+': ' + 'cannot play ' +
                    # choice + ' while an explosion is not active!')
                    return False
            if choice in ['taco', 'watermelon', 'potato', 'beard', 'rainbow']:
                if currHand[choice] < 2:
                    #print('there are not enough '+choice+'s in your hand')
                    return False
                # print('Player ' + str(self.game.currentPlayer) +
                    # ': played ' + choice + ' pair')
            if currHand[choice] < 1:
                #print(choice + ' is not in your hand')
                return False
            return True
        else:
            return False

    def playTurnIndex(self, choice):
        if self.game.isGameOver is False:
            if self.game.explosionStatus is True:
                if self.cards[choice].type != 'defuse':
                    print('Player ' + str(self.game.currentPlayer)+': ' + 'cannot play ' +
                          self.cards[choice].type + ' while an explosion is active!')
                    return

            if choice == 'defuse':
                print('Player ' + str(self.game.currentPlayer)+': ' + 'cannot play ' +
                      choice + ' while an explosion is not active!')
                return

            print('Player ' + str(self.game.currentPlayer) +
                  ': played ' + self.cards[choice].type)

            self.game.playedCards.insert(0, self.cards[choice])
            self.moves.insert(0, self.cards[choice].type)
            temp = {}
            temp[self.game.currentPlayer] = self.cards[choice].type
            self.game.moves.insert(0, temp)
            self.cards.pop(choice)  # self.cards.splice(choice, 1)
            self.game.playedCards[0].render()

        # print('game', self.game)
        # updateDisplay()
        # updateNotice()

    def drawCard(self, num):
        print('Player' + str(self.game.currentPlayer) + ': drawCard')

        if self.game.drawingPile[num].type == 'kitten':
            self.game.drawingPile[num].render()
            self.game.checkGameOver()
        else:
            self.cards.append(self.game.drawingPile[num])
            self.game.drawingPile.pop(num)

            if (num == 0):
                self.moves.insert(0, 'draw')
                temp = {}
                temp[self.game.currentPlayer] = 'draw'
                self.game.moves.insert(0, temp)

                self.game.checkTurns()

        if len(self.game.knownCards0) > 0 and num == 0:
            self.game.knownCards0.pop(0)
        if len(self.game.knownCards1) > 0 and num == 0:
            self.game.knownCards1.pop(0)

        # updateDisplay()
        # updateNotice()

# ----------------------------------------------------------------
#                           COMPUTERAI.py
# ----------------------------------------------------------------


class computerPlayer(object):
    def randomness(self):
        randomValue = random.random()
        if (randomValue < 0.5):
            randomValue += 0.5
        return randomValue

    def __init__(self, game):
        self.game = game
        self.currentCards = {}
        for i in range(len(self.game.player[1].cards)):
            self.currentCards[self.game.player[1].cards[i].type] = 0

        self.currentCards['draw'] = 20
        print(self.currentCards)

        if (self.game.explosionStatus is True):
            if ('defuse' in self.currentCards.keys()):
                self.currentCards['defuse'] = 1000
            else:
                # clearInterval(checkPlayer)
                # clearInterval(countDown)
                self.game.isGameOver = True

            self.currentCards['draw'] = -20000
        else:
            # Evaluate probabilty when explosion status is not true
            if (self.game.explosionStatus is not True):
                if ('defuse' in self.currentCards.keys()):
                    self.currentCards['defuse'] -= 500 * self.randomness()

                if (self.game.player[0].moves[0] == 'skip' or
                        self.game.player[0].moves[0] == 'attack'):
                    if ('see-the-future' in self.currentCards.keys()):
                        self.currentCards['see-the-future'] += 150 * \
                            self.randomness()
                    if ('shuffle' in self.currentCards.keys()):
                        self.currentCards['shuffle'] += 100 * self.randomness()
                    if ('draw-from-bottom' in self.currentCards.keys()):
                        self.currentCards['draw-from-bottom'] += 100 * \
                            self.randomness()
                    if ('skip' in self.currentCards.keys()):
                        self.currentCards['skip'] += 100 * self.randomness()
                    if ('attack' in self.currentCards.keys()):
                        self.currentCards['attack'] += 100 * self.randomness()
                    self.currentCards['draw'] += 80 * self.randomness()

                if (len(self.game.player[0].moves) > 1):
                    if (self.game.player[0].moves[1] == 'see-the-future' and
                            (self.game.player[0].moves[0] == 'skip' or
                                self.game.player[0].moves[0] == 'attack' or
                                self.game.player[0].moves[0] == 'draw-from-bottom')):
                        if ('shuffle' in self.currentCards.keys()):
                            self.currentCards['shuffle'] += 200 * \
                                self.randomness()
                        if ('see-the-future' in self.currentCards.keys()):
                            self.currentCards['see-the-future'] += 50 * \
                                self.randomness()
                        if ('skip' in self.currentCards.keys()):
                            self.currentCards['skip'] += 200 * \
                                self.randomness()
                        if ('draw' in self.currentCards.keys()):
                            self.currentCards['draw'] -= 200
                        if ('draw-from-bottom' in self.currentCards.keys()):
                            self.currentCards['draw-from-bottom'] += 200 * \
                                self.randomness()

                if (self.game.player[0].moves[0] == 'defuse'):
                    if ('see-the-future' in self.currentCards.keys()):
                        self.currentCards['see-the-future'] += 100 * \
                            self.randomness()
                    if ('draw-from-bottom' in self.currentCards.keys()):
                        self.currentCards['draw-from-bottom'] += 80 * \
                            self.randomness()
                    if ('shuffle' in self.currentCards.keys()):
                        self.currentCards['shuffle'] += 100 * self.randomness()
                    self.currentCards['draw'] += 80 * self.randomness()

                if (self.game.player[0].moves[0] == 'draw'):
                    self.currentCards['draw'] += 50 * self.randomness()
                    if ('shuffle' in self.currentCards.keys()):
                        self.currentCards['shuffle'] += 100 * self.randomness()
                    if ('see-the-future' in self.currentCards.keys()):
                        self.currentCards['see-the-future'] += 100 * \
                            self.randomness()

                if (self.game.player[0].moves[0] == 'shuffle'):
                    self.currentCards['draw'] += 1000
                    if ('shuffle' in self.currentCards.keys()):
                        self.currentCards['shuffle'] -= 500 * self.randomness()

                if (len(self.game.playedCards) == 0):
                    self.currentCards['draw'] += 10

                if (1 / len(self.game.drawingPile) > 0.20 and
                        len(self.game.knownCards1) == 0):
                    if (self.currentCards.keys()('see-the-future')):
                        self.currentCards['see-the-future'] += 100 * \
                            self.randomness()

                if (len(self.game.knownCards1) > 0):
                    if ('see-the-future' in self.currentCards.keys()):
                        self.currentCards['see-the-future'] -= 100 * \
                            self.randomness()

                if (self.game.knownCards1[0].type == 'kitten'):
                    # this feels wrong
                    if ('defuse' in self.game.player[0].moves[0]):
                        if ('skip' in self.currentCards.keys()):
                            self.currentCards['skip'] += 200 * \
                                self.randomness()
                        if ('attack' in self.currentCards.keys()):
                            self.currentCards['attack'] += 200 * \
                                self.randomness()
                    else:
                        if ('favor' in self.currentCards.keys()):
                            self.currentCards['favor'] += 200 * \
                                self.randomness()

                    if ('shuffle' in self.currentCards.keys()):
                        self.currentCards['shuffle'] += 100 * self.randomness()
                    if ('draw-from-bottom' in self.currentCards.keys()):
                        self.currentCards['draw-from-bottom'] += 100 * \
                            self.randomness()
                    self.currentCards['draw'] -= 200

                if (len(self.game.player[0].cards) < 4):
                    if (self.currentCards.keys()('favor')):
                        self.currentCards['favor'] += 200 * self.randomness()

                if ('defuse' not in self.currentCards.keys()):
                    if ('favor' in self.currentCards.keys()):
                        self.currentCards['favor'] += 300 * self.randomness()

                if (1 / len(self.game.drawingPile) == 1):
                    self.currentCards['draw'] -= 200

                if (len(self.game.player[1].moves) > 1):
                    if (self.game.player[1].moves[0] == 'see-the-future'):
                        if ('see-the-future' in self.currentCards.keys()):
                            self.currentCards['see-the-future'] -= 500 * \
                                self.self.randomness()

                if (self.game.player[1].moves[0] == 'shuffle'):
                    if ('shuffle' in self.currentCards.keys()):
                        self.currentCards['shuffle'] -= 500 * self.randomness()

        max = ['', -500]
        for key in self.currentCards.keys():
            if (self.currentCards[key] > max[1]):
                max[0] = key
                max[1] = self.currentCards[key]

        print('ai')
        if (max[0] == 'draw'):
            player1Draw()
        else:
            for i in range(len(self.game.player[1].cards)):
                if (self.game.player[1].cards[i].type == max[0]):
                    self.game.player[self.game.currentPlayer].playTurnIndex(i)
                break

    # Use defuse when explosion status is true


# ----------------------------------------------------------------
#                           CARDS.py
# ----------------------------------------------------------------
cardsProperties = {
    'kitten': 'Unless you have a DEFUSE CARD, you\'re dead.',
    'attack': 'End your turn(s) without drawing and force the next player to take 2 turns in a row. (If the victim of an ATTACK CARD plays an ATTACK CARD, their turns are immediately over, and the next player must take 2 turns.)',
    'skip': 'Immediately end your turn without drawing a card. If you play a SKIP CARD as a defense against an ATTACK CARD, it only ends one of the two turns. Two SKIP CARDS would end both turns.',
    'favor': 'Force any other player to give you 1 card from their hand. The cards is randomly assigned.',
    'shuffle': 'Shuffle the Draw Pile without viewing the cards until told to stop. (Useful when you know there\'s an EXPLODING KITTEN coming.)',
    'see-the-future': 'Peek at the top 3 cards from the Draw Pile.',
    'draw-from-bottom': 'Draw a card from the bottom of Draw Pile.',
    'defuse': 'Save yourself from exploding.'
}


class ShuffleCard (object):
    type = 'shuffle'

    def __init__(self, game):
        self.game = game

    def render(self):
        self.game.shuffle()


class ExplodingKittenCard (object):
    def __init__(self, game):
        self.game = game

    type = 'kitten'
    countDown = 0  # WARNING MAY BE INCORRECT
    time = 0  # WARNING MAY BE INCORRECT

    def render(self):
        print('Exploding Started')
        self.game.explosionStatus = True
        # playAudio(0)
        # showExplosive()

        time = 10
        # clearInterval(countDown)
        # countDown = setInterval(def ():
        # time -= 0.1
        # updateTime()
        # print(time);
        # if (time < 0) {
        #     self.game.isGameOver=true
        #     playAudio(1)
        #     self.game.whoWon()
        #     clearInterval(flashKitten)
        #     hideExplosive()
        #     clearInterval(countDown)
        #     #updateDisplay()
        # }
        # }, 100)
        print('Explosing Ended')


class DefuseCard (object):
    type = 'defuse'

    def __init__(self, game):
        self.game = game

    def render(self):
        print('Defuse Cards Started')

        # clearInterval(countDown)
        self.game.explosionStatus = False
        # hideExplosive()

        if self.game.drawingPile[0].type == 'kitten':
            if self.game.currentPlayer == 0:
                # showSelect()
                pass
        else:
            self.game.shuffle()
            self.game.checkTurns()
        print('Defuse Cards Ended')


class SkipCard (object):
    type = 'skip'

    def __init__(self, game):
        self.game = game

    def render(self):
        print('Skip Cards Started')
        self.game.checkTurns()
        print('Skip Cards Ended, current player is', self.game.currentPlayer)


class AttackCard (object):
    type = 'attack'

    def __init__(self, game):
        self.game = game

    def render(self):
        print('Attack Cards Started')
        self.game.switchPlayer()
        if self.game.noOfTurn == 0:
            self.game.noOfTurn += 1
        else:
            self.game.noOfTurn += 2
        print('Attack Cards Ended, current player is', self.game.currentPlayer)


class SeeTheFutureCard (object):
    type = 'see-the-future'

    def __init__(self, game):
        self.game = game

    def render(self):
        print('SeeTheFuture Started')
        if self.game.currentPlayer == 0:
            self.game.knownCards0 = self.game.drawingPile[:3]
        else:
            self.game.knownCards1 = self.game.drawingPile[:3]


class DrawFromBottomCard (object):
    type = 'draw-from-bottom'

    def __init__(self, game):
        self.game = game

    def render(self):
        # print('draw', str(self))
        print('Draw From Bottom Started')
        self.game.player[self.game.currentPlayer].drawCard(
            len(self.game.drawingPile) - 1)
        print('Draw From Bottom  Ended')


class FavorCard (object):
    type = 'favor'

    def __init__(self, game):
        self.game = game

    def render(self):
        print('Favor Cards Started')
        self.game.stealRandom()
        print('Ended Started')


# Cosmetic cats
class TacoCard (object):
    type = 'taco'

    def __init__(self, game):
        self.game = game

    def render(self):
        self.game.stealRandom()


class WatermelonCard (object):
    type = 'watermelon'

    def __init__(self, game):
        self.game = game

    def render(self):
        self.game.stealRandom()


class PotatoCard (object):
    type = 'potato'

    def __init__(self, game):
        self.game = game

    def render(self):
        self.game.stealRandom()


class BeardCard (object):
    type = 'beard'

    def __init__(self, game):
        self.game = game

    def render(self):
        self.game.stealRandom()


class RainbowCard (object):
    type = 'rainbow'

    def __init__(self, game):
        self.game = game

    def render(self):
        self.game.stealRandom()
