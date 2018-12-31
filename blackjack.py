import random

suits = ('♥', '◆', '♠', '♣')
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10,
             'Q':10, 'K':10, 'A':11}

playing = True

class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return '{}{}'.format(self.rank, self.suit)

class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
    
    def __str__(self):
        return str([str(card) for card in self.deck])

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop(0)

class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'A':
            self.aces += 1
    
    def adjust_for_ace(self):
        if self.aces and self.value > 21:
            self.value -= 10
            self.aces -= 1
            
    def __str__(self):
        return str([str(card) for card in self.cards]) + " (" + str(self.value) + ")"

class Chips:
    
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
        self.bet = 0
    
    def lose_bet(self):
        self.total -= self.bet
        self.bet = 0
        
    def __str__(self):
        return("your total: ${}, current bet: ${}".format(self.total, self.bet))

def take_bet(chips):
    bet_made = False
    while not bet_made:
        try:
            bet_taken = int(input("Please enter your bet amount: "))
        except:
            print("Please enter an integer.")
        else:
            if chips.total - bet_taken < 0:
                print("You're poorer than you think! Bet a lower amount! \n")
            else:
                chips.bet = bet_taken
                bet_made = True

def hit(deck,hand):
    hand.add_card(deck.deal())
    print(hand)
    
    while hand.value > 21 and hand.aces:
        print("adjusting for ace")
        hand.adjust_for_ace()
        print(hand)


def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    choice = ''
    while choice != 'hit' or choice != 'stand' or choice != 'h' or choice != 's':
        if hand.value < 21:
            choice = input("hit or stand (h/s): ")
            if choice == 'hit' or choice == 'h':
                hit(deck,hand)
            elif choice == 'stand' or choice == 's':
                playing = False
                break
            else:
                continue
        else:
            playing = False
            break

def show_some(player,dealer):
    print("your hand: {}".format(player))
    dealer_copy = [str(card) for card in dealer.cards]
    dealer_copy[0] = "⬛"
    print("dealer's hand: {}".format(dealer_copy))
    print("\n")
    
def show_all(player,dealer):
    print("your hand: {}".format(player))
    print("dealer's hand: {}".format(dealer))
    print("\n")

def player_busts(player,dealer,chips):
    print('\n\nBust! You lose.')
    chips.lose_bet()
    print("your chip total: ${}".format(chips.total))
    
def player_wins(player,dealer,chips):
    print('\n\nYou win!')
    chips.win_bet()
    print("your chip total: ${}".format(chips.total))
    
def dealer_busts(player,dealer,chips):
    print('\n\nDealer busts! You win!')
    chips.win_bet()
    print("your chip total: ${}".format(chips.total))
    
def dealer_wins(player,dealer,chips):
    print('\n\nDealer wins, you lose!')
    chips.lose_bet()
    print("your chip total: ${}".format(chips.total))
    
def push(player,dealer,chips):
    print('\n\nPush')
    chips.bet = 0
    print("your chip total: ${}".format(chips.total))


# New Game
print('Let\'s Play Blackjack! \n')
player_chips = Chips()
print("Chips: ${}".format(player_chips.total))

print('\nShuffling Deck.....\n')
new_deck = Deck()
new_deck.shuffle()

while True:

    print('\n\n\n')
    
    # Create & shuffle the deck, deal two cards to each player
    player = Hand()
    dealer = Hand()
    player.add_card(new_deck.deal())
    dealer.add_card(new_deck.deal())
    player.add_card(new_deck.deal())
    dealer.add_card(new_deck.deal())
    
    
    # Prompt the Player for their bet
    take_bet(player_chips)
    print('\n\n')

    
    # Show cards (but keep one dealer card hidden)
    show_some(player,dealer)

    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(new_deck,player)
        
             
    # If player's hand exceeds 21, run player_busts() and break out of loop
    if player.value > 21:
        player_busts(player,dealer,player_chips)
        
        
    else:
        # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
        print("\nLet's see what the dealer has...")
        show_all(player,dealer)

        while dealer.value < 17:
            print("\nDealer Hits")
            hit(new_deck,dealer)


        # Show all cards
        print("\nThe final hands!")
        show_all(player,dealer)

        # Run different winning scenarios
        if dealer.value > 21:
            dealer_busts(player,dealer,player_chips)

        elif player.value > dealer.value:
            player_wins(player,dealer,player_chips)

        elif dealer.value > player.value:
            dealer_wins(player,dealer,player_chips)

        else:
            push(player,dealer,player_chips)

    
    # Inform Player of their chips total 
    if player_chips.total == 0:
        print("\n\nThanks for playing, you have no chips left.")
        break
    
    # Ask to play again
    play_again = input("Do you want to play again? (Y/N) ")
    if  play_again == "N" or play_again == 'n' or play_again == 'no':
        print("\n\nThanks for playing!")
        print("Chips: ${}".format(player_chips.total))
        break
    else:
        playing = True
        if len(new_deck.deck) < 20:
            print('\nReshuffling Deck.....\n')
            new_deck = Deck()
            new_deck.shuffle()
        continue
        




