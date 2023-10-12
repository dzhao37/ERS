import random

class Card:
    """
    This class is the building block for Player and Pile classes.

    Attributes:
        value (str): The number/letter on the card.
        suit (str): The suit of the card.
    """

    def __init__(self, value, suit):
        """
        The constructor for Card class.

        Parameters:
            value (str): The number/letter on the card.
            suit (str): The suit of the card.
        """
        
        self.value = value
        self.suit = suit

    def __str__(self):
        """
        The function to print a Card object.
          
        Returns:
            A string containing its value followed by the suit.
        """

        return f"({self.value}, {self.suit})"
    
    def is_face_card(self):
        """
        This function checks if a card is a Jack, Queen, King, or Ace.
          
        Returns:
            A boolean.
        """

        if(self.value == "Ace" or self.value == "King" or self.value == "Queen" or self.value == "Jack"):
            return True
        else:
            return False

# create an instance for each player
class Player:
    """
    This class represents the player and their data.
        
    Attributes:
        player (int): The order in which the players will play.
        hand (list): A list of Card objects held by the player.
    """
    
    def __init__(self, player, hand):
        """
        The constructor for Player class.

        Parameters:
            player (int): The order in which the players will play.
            hand (list): A list of Card objects held by the player.
        """

        self.player = player
        self.hand = hand # list of card objects

    def draw_card(self, pile):
        """
        This function draws the top card from the player hand and puts it in the pile.

        Parameters:
            pile (Pile): The middle pile of Card objects.

        Returns:
            card (Card): The card drawn.
        """
        
        # prevents drawing from an empty hand
        if(len(self.hand) >= 1):
            card = self.hand[0]
            if(isinstance(card, Card)):
                print(f"Player {self.player}: {card}")
                if(isinstance(pile, Pile)):
                    # remove the top card of the hand and add it to the pile
                    pile.add_card_to_pile(card)
                    self.hand.remove(card)
                    return card
        
        # if the hand is empty, return a Joker card to indicate that someone won
        return Card("Joker", "Joker")

# represents the middle pile
class Pile:
    """
    This class represents the middle pile of cards.
        
    Attributes:
        pile (list): A list of Card objects in the middle pile.
    """

    def __init__(self, pile):
        """
        The constructor for Pile class.

        Parameters:
            pile (list): A list of Card objects in the middle pile.
        """

        self.pile = pile

    def add_card_to_pile(self, card):
        """
        This function appends the given card to the middle pile. It does not remove a card from the player hand.

        Parameters:
            card (Card): The top card drawn from the player's hand.
        """

        if(isinstance(card, Card)):
            # since index 0 is the top card and -1 is the bottom card, reverse, append the card, and then reverse again
            self.pile.reverse()
            self.pile.append(card)
            self.pile.reverse()

    # slap rule that allows the player to take the pile if the top and second to top card are the same
    def is_double(self):
        """
        This function checks if the top two cards are the same.

        Returns:
            A boolean.
        """

        top_card = self.pile[-1]
        second_card = self.pile[-2]
        if(isinstance(top_card, Card) and isinstance(second_card, Card)):
            if(top_card.value == second_card.value):
                return True
            else:
                return False

    # slap rule that allows the player to take the pile if the top and third to top card are the same
    def is_sandwich(self):
        """
        This function checks if the top card and third to top card are the same.

        Returns:
            A boolean.
        """

        top_card = self.pile[-1]
        third_card = self.pile[-3]
        if(isinstance(top_card, Card) and isinstance(third_card, Card)):
            if(top_card.value == third_card.value):
                return True
            else:
                return False

    # slap rule that allows the player to take the pile if the top card is a King and the second to top card is a Queen or vice versa
    def is_marriage(self):
        """
        This function checks if the top two cards are King and Queen respectively or vice versa.

        Returns:
            A boolean.
        """

        top_card = self.pile[-1]
        second_card = self.pile[-2]
        if(isinstance(top_card, Card) and isinstance(second_card, Card)):
            if((top_card.value == "King" and second_card.value == "Queen") or (top_card.value == "Queen" and second_card.value == "King")):
                return True
            else:
                return False

    # returns true if any of the rules are met
    def is_valid_slap(self):
        """
        This function checks if a slap is valid.

        Returns:
            A boolean.
        """

        # only check for a valid slap if the pile has 2 or more cards
        if(len(self.pile) >= 2):
            if(self.is_double() or self.is_marriage()):
                return True
        if(len(self.pile) >= 3):
            if(self.is_sandwich()):
              return True
        return False

#---------------------------------------------------------------------------------------------------------------------------------------
# main functions

# randomizes order of the initial deck before dealing to the players
def shuffle_deck(deck):
    x = 0
    while x < len(deck) - 1:
        # choose a random index and swap places with the current index if the indexes are different
        r = random.randint(0,51)
        if deck[x] == deck[r]:
            continue
        else:
            deck[x], deck[r] = deck[r], deck[x]
            x += 1

# def deal_cards(num_play):
#     hand1, hand2 = [], []
#     while len(deck) > 0:
#         hand1.append(deck[0])
#         deck.remove(deck[0])
#         hand2.append(deck[0])
#         deck.remove(deck[0])
#     player1 = Player(1, hand1)
#     player2 = Player(2, hand2)

# given a face card, returns the number of times the other player should draw 
def count_times(card):
    if(isinstance(card, Card)):
        if(card.value == "Ace"):
            times = 4
        elif(card.value == "King"):
            times = 3
        elif(card.value == "Queen"):
            times = 2
        elif(card.value == "Jack"):
            times = 1
        return times

# player who did not place the face card draws x amount of times until they draw a face card or draw all number cards
def do_face_card(player_turn, times):
    if(player_turn == player1):
        player_drawing = player2
    elif(player_turn == player2):
        player_drawing = player1

    x = 0
    while x < times:
        current_card = player_drawing.draw_card(pile1)
        # checks for an empty hand and invalid slap to ensure that the game is over
        if(is_game_over() and not pile1.is_valid_slap()):
            x = times
            break

        # if a face card is drawn, return appropriate input data for the next executino of do_face_card, otherwise keep drawing
        if(current_card.is_face_card()):
            return player_drawing, current_card
        else:
            x += 1
    
    # if only number cards are drawn, add the pile to the bottom of the hand of the player who drew the face card
    player_turn.hand += pile1.pile
    # clear the pile
    pile1.pile = []
    # return the person drawing so the person who drew the face card starts the round again and number card to indicate the round has been won
    return player_drawing, current_card

# if either player's hand is empty, return true
def is_game_over():
    game_over = False
    if(len(player1.hand) == 0 or len(player2.hand) == 0):
        game_over = True
    return game_over

#---------------------------------------------------------------------------------------------------------------------------------------
# initializing

# create a full deck
deck = []
for suit in ['\u2666','\u2665','\u2663','\u2660']:
    for value in ['Ace','2', '3','4','5','6','7','8','9','10','Jack','Queen','King']:
        deck.append(Card(value, suit))

shuffle_deck(deck)

# num_players = int(input("Please enter the number of players: "))
# deal_cards(num_players)

# deal the top card, alternating between player hands
hand1, hand2 = [], []
while len(deck) > 0:
    hand1.append(deck[0])
    deck.remove(deck[0])
    hand2.append(deck[0])
    deck.remove(deck[0])
player1 = Player(1, hand1)
player2 = Player(2, hand2)

#---------------------------------------------------------------------------------------------------------------------------------------
# gameplay

player_turn = player1
no_winner = True
pile1 = Pile([])
print("Start!")
print("Player 1 # of cards: ", len(player1.hand))
print("Player 2 # of cards: ", len(player2.hand))
while no_winner:
    current_card = player_turn.draw_card(pile1)
    
    # checks for an empty hand and invalid slap to ensure that the game is over
    if(is_game_over() and not pile1.is_valid_slap()):
        no_winner = False
        break

    if(current_card.is_face_card()):
        print("Face card chain!")
        times = count_times(current_card)
        player_turn, current_card = do_face_card(player_turn, times)

        pile_won = True
        # if the last card played was a face card...
        if(current_card.is_face_card()):
            pile_won = False
        
        # ... keep executing do_face_card and switch players each time
        while not pile_won:
            times = count_times(current_card)
            player_turn, current_card = do_face_card(player_turn, times)

            # if the last card was a number card, exit the loop
            if(not current_card.is_face_card()):
                pile_won = True
        
        if(player_turn == player1):
            print("Player 2 won the round!")
        elif(player_turn == player2):
            print("Player 1 won the round!")
        print("Player 1 # of cards: ", len(player1.hand))
        print(f"Player 2 # of cards: {len(player2.hand)}\n")

        if(is_game_over()):
            no_winner = False
    
    # switch player turn
    if(player_turn == player1):
        player_turn = player2
    elif(player_turn == player2):
        player_turn = player1

#---------------------------------------------------------------------------------------------------------------------------------------
# end game

if(len(player1.hand) == 0):
    print("Player 2 wins!")
elif(len(player2.hand) == 0):
    print("Player 1 wins!")