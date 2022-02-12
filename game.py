from random import shuffle
from sys import argv

# Set up the suits (A list of chr codes is at https://inventwithpython.com/charactermap):
HEARTS = chr(9829) # '♥'
DIAMONDS = chr(9830) # '♦'
SPADES = chr(9824) # '♠'
CLUBS = chr(9827) # '♣'
BACKSIDE = 'backside'
BLACK = '\033[48;5;255m\033[38;5;0m'
RED = '\033[48;5;255m\033[38;5;160m'
RESET = '\033[0;0m'

try: 
    DECKS = int(argv[1])
except:
    DECKS = 1

try:
    RESHUFFLE = int(argv[2])
except:
    RESHUFFLE = 12

suits = (HEARTS, DIAMONDS, SPADES, CLUBS)
ranks = ('2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10', 'J ', 'Q ', 'K ', 'A ')
values = {'2 ' : 2, '3 ' : 3, '4 ' : 4, '5 ' : 5, '6 ' : 6, '7 ' : 7, '8 ' : 8, '9 ' : 9, '10' : 10, 'J ' : 10, 'Q ' : 10, 'K ' : 10, 'A ' : 11}

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

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
    
    def add_card(self, card):
        self.cards.append(card)
        game.burned_cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'A ':
            self.aces += 1

    def adjust_for_aces(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
        
class Pot:
    def __init__(self):
        self.total = 10000
        self.bet = 0

    def win_bet(self):
        if game.player.cards[0].rank == 'A ' or game.player.cards[1].rank == 'A ':
            self.total += 1.5*self.bet # 3/2 for blackjack
        else:
            self.total += self.bet
            
    def lose_bet(self):
        self.total -= self.bet


class Game:
    def __init__(self):
        self.pot = Pot()
        self.deck = []
        self.deck = Deck()
        self.burned_cards = []
        
    def game(self):
        while self.pot.total > 0:
            if len(self.deck.deck) <= RESHUFFLE:
                self.deck = []
                self.deck = Deck()
                self.deck.shuffle()
                self.running_count = 0
                self.true_count = 0
                self.burned_cards = []
                self.play_round()
            else:
                self.play_round()
        self.game_over()

    def play_round(self):
        self.dealer = Hand()
        self.player = Hand()

        self.player.add_card(self.deck.deal())
        self.dealer.add_card(self.deck.deal())
        self.player.add_card(self.deck.deal())
        self.dealer.add_card(self.deck.deal())

        self.pot.bet = self.take_bet()
        self.show_some()
        
        global playing
        while True:
            self.hit_or_stand(self.player)
            self.show_some()
            
            if self.player.value > 21:
                self.player_bust(self.pot)
                break

        if self.player.value <= 21:
            while self.dealer.value < 17:
                self.hit(self.dealer)
            
            self.show_all()

            if self.dealer.value > 21:
                self.dealer_busts(self.pot)
            elif self.dealer.value > self.player.value:
                self.dealer_wins(self.pot)
            elif self.player.value > self.dealer.value:
                self.player_wins(self.pot)
            
            if self.player.value > 21:
                self.player_bust(self.pot)
        
        print("\nPlayer's winnings stand at: ", self.pot.total)
        playing = False
        

    def take_bet(self):
        while True:
            try:
                self.pot.bet = int(input("\nHow much would you like to bet?\n"))
            except ValueError:
                print("Sorry! Please enter a number:\n")
            else:
                if self.pot.bet > self.pot.total:
                    print("You cannot exceed your pot!:\n")
                else: 
                    break

    def hit(self, hand):
        hand.add_card(self.deck.deal())
        hand.adjust_for_aces()
        
    def hit_or_stand(self, hand):
        global playing
        while True:
            ask = input("\nWould you like to hit or stand? [h/s]\n")
            if ask[0].lower() == 'h':
                self.hit(hand)
            elif ask[0].lower() == 's':
                print("\nStand! Dealer's turn!\n")
            else:
                print("\nSorry I did not understand that! Please try again...\n")
            break

    def show_some(self):
        print("\nDealer's hand:\n")
        print("{}|###|{}".format(RED, RESET), "{} ".format(RED) + str(self.dealer.cards[1]) + " {}".format(RESET))
        print("\nPlayer's hand:\n", *self.player.cards, sep='\n')

    def show_all(self):
        print("\nDealer's hand:\n", *self.dealer.cards, sep='\n')
        print("\nDealer's hand = ", self.dealer.value)
        print("\nPlayer's hand:\n", *self.player.cards, sep='\n')
        print("\nPlayer's hand = ", *self.player.value)

    def player_bust(self, bet):
        print("YOU LOSE")
        bet.lose_bet()

    def player_wins(self, bet):
        print("YOU WIN")
        bet.win_bet()

    def dealer_busts(self, bet):
        print("YOU WIN")
        bet.win_bet()

    def dealer_wins(self, bet):
        print("DEALER WINS")
        bet.lose_bet()

    def push(self):
        print("It's a Tie")
    
    def count_running(self):
        if self.turned_card.rank in ['2 ', '3 ', '4 ', '5 ', '6 ']:
            self.running_count += 1
        elif self.turned_card.rank in ['A ', 'J ', 'Q ', 'K ', '10']:
            self.running_count -= 1
        else:
            self.running_count += 0

    def count_true(self):
        self.decks_remaining = round(((len(self.deck.deck)/52)*2))/2
        self.true_count = round((self.running_count / self.decks_remaining)*2)/2
        return self.true_count

    def game_over(self):
        rematch = input("Would you like to play again? [Y/N]\n")
        if rematch[0].upper() == 'Y':
            print("")
            game = Game()
            game.game()
        else:
            quit()


if __name__ == "__main__":
    game = Game()
    game.game()