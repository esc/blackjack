import random
import time

DELAY = 0.5
SUITS = ["hearts", "diamonds", "clubs", "spades"]
NAMES_SCORES = [
    ("one",   1),
    ("two",   2),
    ("three", 3),
    ("four",  4),
    ("five",  5),
    ("six",   6),
    ("seven", 7),
    ("eight", 8),
    ("nine",  9),
    ("ten",   10),
    ("jack",  10),
    ("queen", 10),
    ("king",  10),
    ("ace",  (11, 1)),
]


class Card(object):
    """ A card in the game.

    Attributes
    ----------
    name: str
        name of the card
    suit: str
        suit of the card
    primary_score: int
        the primary score of the card
    secondary_score: int
        the secondary score of the card, only for aces

    """

    def __init__(self, name, suit, score):
        self.name = name
        self.suit = suit
        if isinstance(score, tuple):
            self.primary_score = score[0]
            self.secondary_score = score[1]
        else:
            self.primary_score = score
            self.secondary_score = score

    def __str__(self):
        return "{} of {}".format(self.name, self.suit)

    def __repr__(self):
        if self.primary_score == self.secondary_score:
            score = self.primary_score
        else:
            score = (self.primary_score, self.secondary_score)
        return "Card({}, {}, {})".format(self.name, self.suit, score)

class Deck(object):
    """ A deck of cards.

    This deck will never run out, in case all 52 cards are exhausted, a fresh
    set is created. Quasi an infinity deck.

    Attributes
    ----------
    cards: List of Cards
        The cards left in the deck.

    """

    def __init__(self):
        self.init_cards()

    def init_cards(self):
        """ Initialise a fresh set of cards. """
        self.cards = [Card(name, suit, score)
                    for suit in SUITS
                    for (name, score) in NAMES_SCORES]
        random.shuffle(self.cards)

    def draw(self):
        """ Pop a single card from the deck. """
        if len(self.cards) == 0:
            self.init_cards()
        return self.cards.pop()


class Hand(object):
    """ The hand of a player/dealer.

    Attributes
    ----------
    cards: List of Cards
        The cards in hand.

    """

    def __init__(self):
        self.cards = []

    def __str__(self):
        return str([str(c) for c in self.cards])

    def add(self, card):
        """ Add a card to the hand. """
        self.cards.append(card)

    def score(self):
        """ Compute the score of this hand. """
        s = sum((c.primary_score for c in self.cards))
        if s > 21:
            s = sum((c.secondary_score for c in self.cards))
        return s


class Game(object):
    """ The game itself. 

    Contains all attributes and methods to hold and operate on the game state.
    """

    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()

    def player_setup(self):
        """ Initialise the player hand. """
        self.player_hand.add(self.deck.draw())
        self.player_hand.add(self.deck.draw())

    def player_round(self):
        """ Do a player round. """
        while True:
            # print status
            print("Player hand is: {}".format(str(self.player_hand)))
            player_score = self.player_hand.score()
            print("Player score is: {}".format(player_score))
            # check if player looses
            if player_score > 21:
                print("You loose!")
                return False
            # request input
            print("draw? (y/n)")
            response = input()
            if response == "y":
                # add another card
                self.player_hand.add(self.deck.draw())
            elif response == "n":
                # player is done
                return True

    def dealer_setup(self):
        """ Initialise the dealer hand. """
        self.dealer_hand.add(self.deck.draw())
        self.dealer_hand.add(self.deck.draw())

    def dealer_round(self):
        """ Do a dealer round. """
        player_score = self.player_hand.score()
        while True:
            # print status
            print("Dealer hand is: {}".format(str(self.dealer_hand)))
            dealer_score = self.dealer_hand.score()
            print("Dealer score is: {}".format(dealer_score))
            time.sleep(DELAY)
            if dealer_score > 21:
                # check if the dealer drew too much
                print("You win!")
                break
            elif dealer_score >= player_score:
                # check if the dealer wins
                print("You loose!")
                break
            else:
                # dealer must draw more
                time.sleep(DELAY)
                print("Dealer will draw again...")
                self.dealer_hand.add(self.deck.draw())

    def play(self):
        """ Play a game. """
        print("Starting new game...")
        # do the player round
        self.player_setup()
        still_playing = self.player_round()
        if still_playing:
            # do the dealer round
            self.dealer_setup()
            self.dealer_round()

game = Game()
game.play()
