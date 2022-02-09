from random import shuffle, randint
from sys import argv

# Set up the suits (A list of chr codes is at https://inventwithpython.com/charactermap):
HEARTS = chr(9829) # '♥'
DIAMONDS = chr(9830) # '♦'
SPADES = chr(9824) # '♠'
CLUBS = chr(9827) # '♣'
BACKSIDE = 'backside'

try: 
    DECKS = int(argv[1])
except:
    DECKS = 1

suits = (HEARTS, DIAMONDS, SPADES, CLUBS)
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
values = {'2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9, '10' : 10, 'J' : 10, 'Q' : 10, 'K' : 10, 'A' : 11}


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return self.rank + self.suit
        

class Deck:
    def __init__(self):
        self.deck = []
        for i in range(DECKS): 
            for suit in suits:
                for rank in ranks:
                    self.deck.append(Card(suit, rank))
                
    def __str__(self):
        deck_contents = ''
        x = 0
        for card in self.deck:
            x += 1
            deck_contents += '\n' + card.__str__()
        return "The deck has: " + deck_contents

    def shuffle(self):
        shuffle(self.deck)

    def deal(self):
        dealt_card = self.deck.pop()
        return dealt_card
     

class Game:
    def __init__(self):
        self.deck = Deck() 
        self.deck.shuffle() 
        self.running_count = 0

    def play_round(self):
        for i in range(randint(1,20)):
            turned_card = self.deck.deal()
            print(turned_card)
            if turned_card.rank in ['2', '3', '4', '5', '6']:
                self.running_count += 1
            elif turned_card.rank in ['A', 'J', 'Q', 'K', '10']:
                self.running_count -= 1
            else:
                self.running_count += 0
        return self.running_count

    def check_count(self):
        try:
            self.player_count = int(input("What is the running count?\n"))
        except:
            print("You must enter a count!\n")
            self.player_count = int(input("What is the running count?\n"))
        

        if self.player_count == self.running_count:
            print("Good Job!\n")
        else:
            print("Not quite!\nThe running count was {}\n".format(self.running_count))

if __name__ == "__main__":
    game = Game()
    
    while len(game.deck.deck) > 0:
        game.play_round()
        game.check_count()