from random import shuffle, randint
from sys import argv

# Set up the suits (A list of chr codes is at https://inventwithpython.com/charactermap):
HEARTS = chr(9829) # '♥'
DIAMONDS = chr(9830) # '♦'
SPADES = chr(9824) # '♠'
CLUBS = chr(9827) # '♣'

try: 
    DECKS = int(argv[1])
except:
    DECKS = 1

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
        if len(self.deck) > 0: 
            dealt_card = self.deck.pop()
            return dealt_card


class Game:
    def __init__(self):
        self.deck = Deck() 
        self.deck.shuffle() 
        self.running_count = 0

    def play_round(self):
        for i in range(randint(1,len(self.deck.deck))):
            turned_card = self.deck.deal()
            if turned_card.suit == CLUBS or turned_card.suit == SPADES:
                print(f"\033[48;5;255m\033[38;5;0m {turned_card} \033[0;0m")
            if turned_card.suit == HEARTS or turned_card.suit == DIAMONDS:
                  print(f"\033[48;5;255m\033[38;5;160m {turned_card} \033[0;0m")  
            if turned_card.rank in ['2 ', '3 ', '4 ', '5 ', '6 ']:
                self.running_count += 1
            elif turned_card.rank in ['A ', 'J ', 'Q ', 'K ', '10']:
                self.running_count -= 1
            else:
                self.running_count += 0
        return self.running_count

    def check_count(self):
        try:
            self.player_count = int(input("\nWhat is the running count?\n"))
        except:
            print("You must enter a count!\n")
            self.player_count = int(input("What is the running count?\n"))
        

        if self.player_count == self.running_count:
            print("Good Job!\n")
        else:
            print("Not quite!\nThe running count was {}\n".format(self.running_count))

    def game(self):
        while len(self.deck.deck) > 0:
            self.play_round()
            self.check_count()
        self.game_over()

    def game_over(self):
        rematch = input("Would you like to play again? [Y/N]\n")
        if rematch == 'Y' or rematch == 'y' or rematch == 'Yes' or rematch == 'yes':
            print("")
            game = Game()
            game.game()
        else:
            quit()


if __name__ == "__main__":
    game = Game()
    game.game()