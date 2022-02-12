from random import shuffle, randint
from sys import argv
from time import sleep

# Set up the suits (A list of chr codes is at https://inventwithpython.com/charactermap):
HEARTS = chr(9829) # '♥'
DIAMONDS = chr(9830) # '♦'
SPADES = chr(9824) # '♠'
CLUBS = chr(9827) # '♣'

CURSOR_UP_ONE = '\033[1A' 
ERASE_LINE = '\033[2K'

try: 
    DECKS = int(argv[1])
except:
    DECKS = 6

try:
    TIME = int(argv[2])
except:
    TIME = 3

suits = (HEARTS, DIAMONDS, SPADES, CLUBS)
ranks = ('2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10', 'J ', 'Q ', 'K ', 'A ')


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

    def shuffle(self):
        shuffle(self.deck)

    def deal(self):
        if len(self.deck) > 0: 
            dealt_card = self.deck.pop()
            return dealt_card


class Game:
    def __init__(self):
        self.deck = Deck() 
        self.deck.shuffle() 
        self.running_count = 0
        self.true_count = 0
        self.burned_cards = []

    def play_round(self):
        for i in range(randint(1,min(26,len(self.deck.deck)))):
            self.turned_card = self.deck.deal()
            if self.turned_card.suit == CLUBS or self.turned_card.suit == SPADES:
                print(f"\033[48;5;255m\033[38;5;0m {self.turned_card} \033[0;0m")
            elif self.turned_card.suit == HEARTS or self.turned_card.suit == DIAMONDS:
                print(f"\033[48;5;255m\033[38;5;160m {self.turned_card} \033[0;0m")  
            
            self.count_running()            
            self.burned_cards.append(self.turned_card)
            sleep(1)
                  
        return self.running_count, self.burned_cards

    def count_running(self):
        if self.turned_card.rank in ['2 ', '3 ', '4 ', '5 ', '6 ']:
            self.running_count += 1
            sleep(TIME)
            print("+1")
        elif self.turned_card.rank in ['A ', 'J ', 'Q ', 'K ', '10']:
            self.running_count -= 1
            sleep(TIME)
            print("-1")
        else:
            self.running_count += 0
            sleep(TIME)
            print("-")
        return self.running_count

    def count_true(self):
        self.decks_remaining = round(((len(self.deck.deck)/52)*2))/2
        if self.decks_remaining > 0:
            self.true_count = round((self.running_count / self.decks_remaining)*2)/2
        else:
            self.true_count = 0
        return self.true_count

    def check_count(self):
        try:
            self.player_count = int(input("\nWhat is the running count?\n"))
        except:
            print("You must enter a count!")
            self.check_count()
        
        if self.player_count == self.running_count:
            print("Good Job!\n")
        else:
            print("Not quite!\nThe running count is {}\n".format(self.running_count))

    def check_true_count(self):
        self.count_true()
        try:
            self.player_true_count = float(input("\nWhat is the true count?\n"))
        except:
            print("You must enter a count!")
            self.check_true_count()

        if self.player_true_count == self.true_count:
            print("Good Job!\n")
        else:
            print("Not quite!\nThe true count is {}\n".format(self.true_count))

    def game(self):
        while len(self.deck.deck) > 0:
            self.play_round()
            self.check_count()
            self.check_true_count()
        self.game_over()

    def game_over(self):
        rematch = input("Would you like to play again? [Y/N]\n")
        if rematch[0].upper() == 'Y':
            print("")
            game = Game()
            game.game()
        else:
            quit()

    def print_burned(self):
        for card in self.burned_cards:
            if card.suit == CLUBS or card.suit == SPADES:
                print(f"\033[48;5;255m\033[38;5;0m {card} \033[0;0m")
            elif card.suit == HEARTS or card.suit == DIAMONDS:
                print(f"\033[48;5;255m\033[38;5;160m {card} \033[0;0m")


if __name__ == "__main__":
    game = Game()
    game.game()