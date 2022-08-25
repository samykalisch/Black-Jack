## Blackjack V 1.0
## Samuel Kalisch Yanez
## August 2022

import random as r
import time as t
import os

class Card(object):
  def __init__(self, suit, face):
    self.suit = suit
    self.face = face

  @property
  def suit(self):
    return self.__suit
    
  @suit.setter
  def suit(self, value):
    if  value not in ['Spades','Clubs','Diamonds','Hearts']: 
      raise ValueError("Suit is not in the game.")
    self.__suit = value 
    
  @property
  def face(self):
    return self.__face
    
  @face.setter
  def face(self, value):
    if value not in ['A',2,3,4,5,6,7,8,9,10,'J','Q','K']: 
      raise ValueError("Face is not in the game.")
    self.__face = value
  
  def get_value(self):
    values = {'A':1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:10,'J':10,'Q':10,'K':10} 
    return values[self.face]   
  
  def get_image(self):
    suits = {'Spades': '♠','Clubs':'♣','Diamonds': '♦','Hearts':'♥'}
    ls =  ['_______________', 
        '|             |',
        f'| {self.face: <2}          |',
        '|             |',
        '|             |',
        '|             |',
        f'|      {suits[self.suit]}      |',
        '|             |',
        '|             |',
        '|             |',
        f'|          {self.face: >2} |',
        '|_____________|']
    
    return ls
     
  def __str__(self): 
    return f'{self.face: <2} of {self.suit}'
    
class DeckOfCards(object): 
  def __init__(self, number_of_decks = 1):
    self.__cards= []
    self.add_cards(display_text=False)
  
  def add_cards(self, number_of_decks = 1, display_text = True):
    suits = ['Spades','Clubs','Diamonds','Hearts']
    faces = ['A',2,3,4,5,6,7,8,9,10,'J','Q','K']
    for n in range(number_of_decks):
      for s in suits:
        for f in faces:
          self.__cards.append(Card(s,f))
    
    if display_text:
      print()
      print("The deck has been restocked.")
      print()
      t.sleep(.5)
           
  def get_lenght(self):
    return len(self.__cards)

  def shuffle(self, display_text = True):
    r.shuffle(self.__cards)
    if display_text:
      print("Deck is being shuffled...")
      t.sleep(1)
      print("Deck shuffled succefully.")
      print()
  
  def pop_cards(self, num_crads = 1):
    if num_crads > self.get_lenght():
      raise ValueError("You do not have enough card to pop.")
    return [self.__cards.pop() for i in range(num_crads)]

  def __str__(self):
    return str([str(i) for i in self.__cards])
      
class Dealer:
  def __init__(self, name = 'Dealer'):
    self.name = name
    self.hand = []
  
  def reset_hand(self):
    self.hand.clear()
    
  def draw_cards(self,deck,num_cards =1):
    if num_cards >= deck.get_lenght():
      deck.add_cards()
      deck.shuffle()
      t.sleep(1)
    
    for i in deck.pop_cards(num_cards): self.hand.append(i)
    
  def get_score(self):       
    has_ace = False
    for c in self.hand:
      if c.face == 'A':
        has_ace = True
        break
    
    score = sum([i.get_value()  for i in self.hand])
    if has_ace == True and score < 12: score +=10
    
    return score
  
  def print_info(self, show_score = True, hidden = False):
    hidden_icon =  ['_______________', 
                    '|             |',
                    '| ?           |',
                    '|             |',
                    '|             |',
                    '|             |',
                    '|      ?      |',
                    '|             |',
                    '|             |',
                    '|             |',
                    '|           ? |',
                    '|_____________|']
    cards= [i.get_image() for i in self.hand]
    
    if hidden: cards[-1] = 'hidden'
    
    # prints cards
    print(self.name + ': ', '\n')
    for i in range(12):
      for j in range(len(cards)):
        if cards[j] == 'hidden':
          print(hidden_icon[i], end = '\t')
        else:
          print(cards[j][i], end = '\t')
      print()
      
    print()
    if show_score: print(f'{self.name} score: {self.get_score()}\n')
    
  def print_info_V1(self, hidden = False):
    cards= [str(i)for i in self.hand]
    
    if hidden: cards[-1] = 'hidden'

    print(str(self.name) + ': '+ str(cards)+ '\n')
  
  def __str__(self):
    return str(self.name) + ': ' + str([str(i) for i in self.hand])

class Player(Dealer):
  def __init__(self, name, money, bet):
    super().__init__(name)
    self.money = money
    self.bet = bet
    
  @property
  def money(self):
    return self.__money
  
  @money.setter
  def money(self, money):
    if 0  > money:
      raise ValueError("Cannot have negative money.")
    self.__money = money
    
  @property
  def bet(self):
    return self.__bet
  
  @bet.setter
  def bet(self,bet):
    if 0 > bet:
      raise ValueError("Cannot have a negatice bet.")
    elif bet > self.__money: 
      raise ValueError("Cannot have a bet higher than the money.")
    else:
      self.__bet = bet
  
  def ask_for_card(self, split = False, insurance = False):
    moves = ['h','x','d']
    move = input('Enter option: ')
    
    while move not in moves:
      print('\nPlease enter a correct output.\n')
      move = input('Enter option: ')
      
    return move

class Game:
  def __init__(self):
    self.deck = DeckOfCards()
    self.player = Player('Player 1', 0, 0)
    self.dealer = Dealer()

  def gameV1(self): 
    # -------------- clear terminal -------------- 
    self.clear()
    
    # -------------- greetings -------------- 
    print(50*'-','\n')
    print('Hello! Welcome to Kalisch\'s 21 Black Jack')
    self.player.money = self.ask_numeric('Enter amount of money: ')
    print()
    
    # -------------- shuffles deck -------------- 
    self.deck.shuffle()
    
    # --------------  game repeats until player has no money -------------- 
    while self.player.money > 0:
      
      # -------------- asks for bet, breaks if player dosn't bet --------------
      t.sleep(1)
      print(50*'-','\n')
  
      bet = self.ask_numeric(f'Press enter a bet to start game (max: ${self.player.money}, end: $0): ') 
      while bet > self.player.money:
        bet = self.ask_numeric(f'Press enter a bet to start game (max: ${self.player.money}, end: $0): ') 
      self.player.bet = bet
      print()
      if self.player.bet == 0: break  

      # -------------- give initital cards-------------- 
      t.sleep(1)
      print(50*'-','\n')
      
      self.player.draw_cards(self.deck)
      self.player.print_info(show_score=False)
      
      t.sleep(1)
      self.dealer.draw_cards(self.deck)
      self.dealer.print_info(show_score=False)
      
      t.sleep(1)
      self.player.draw_cards(self.deck)
      self.player.print_info(show_score=False)
      
      t.sleep(1)
      self.dealer.draw_cards(self.deck)
      self.dealer.print_info(show_score = False, hidden='True')
      print(50*'-','\n')
      
      
      # -------------- give cards to player --------------
      t.sleep(2)
      self.player.print_info()
      if self.player.get_score() != 21: print('Moves:\nh: hit\nd: double\nx: stay')
      while self.player.get_score() < 21:
        ask = self.player.ask_for_card()
        
        t.sleep(1)
        print()
        
        if ask == 'h': 
          self.player.draw_cards(self.deck)
          self.player.print_info()
       
        elif ask == 'd': 
          if self.player.bet*2 >self.player.money: 
            print('You do not have enough money to double.','\n')
            continue
          
          self.player.bet*=2 
          self.player.draw_cards(self.deck)
          self.player.print_info()
          break 
        
        else: 
          break
      
      # -------------- give cards to dealer -------------- 
      if self.player.get_score() < 22:
        print(50*'-','\n')
        t.sleep(1)
        self.dealer.print_info()
        t.sleep(1)
        
        while self.dealer.get_score() < 17:
          self.dealer.draw_cards(self.deck)
          t.sleep(1)
          self.dealer.print_info()
      
      # -------------- decide the winner -------------- 
      
      self.decide_winner()
      
      # -------------- reset game and clear terminal -------------- 
      print(f'Your balance is ${self.player.money}.')
      input("ENTER FOR NEXT GAME: ") 
      self.player.reset_hand()
      self.dealer.reset_hand()
      self.clear()
      
    # thank you
    t.sleep(1)
    print(50*'-','\n')
    print(f'You are elegible to cash out ${self.player.money}.')
    print('Thanks for playing Kalisch\'s 21 Black Jack!!!', '\n\n'+ 50*'-','\n')  
  
  def decide_winner(self) :   
    # frequently used conditions memorized
    dealer_score=  self.dealer.get_score()
    player_score = self.player.get_score()
    dealer_bj = True if len(self.dealer.hand) == 2 and dealer_score == 21 else False 
    player_bj = True if len(self.player.hand) == 2 and player_score == 21 else False
    
    # change bet if player bj
    if player_bj: self.player.bet *= round(self.player.bet*1.5)
    
    # show scores on the screen 
    print(50*'-','\n')
    t.sleep(1)
    print(f'Player score: {player_score}')
    print(f'Dealer score: {dealer_score}')
    print()
    t.sleep(1)
    
    # win/loss by blackjack
    if dealer_bj and not player_bj: result = False
    elif player_bj and not dealer_bj: result = True
    
    # win/loss by overshooting
    elif player_score > 21: result = False
    elif dealer_score > 21: result = True 
     
    # win/loss by better score
    elif dealer_score > player_score: result = False
    elif dealer_score < player_score: result = True
    
    # tie
    else: result = None

    if result:
      print(f'Congratulation you have won ${self.player.bet}!!!')
      self.player.money += self.player.bet
      
    elif result == None:
      print(f'The game has ended in a tie.')
      
    else:
       print(f'You\'ve lost the ${self.player.bet} bet.')
       self.player.money -= self.player.bet
      
    print('\n' + 50*'-','\n')  
     
  def clear(self):
    os.system("clear")
    
  def check_blackjack(self):
      if get_score(player) == 21 and get_score(player) != 21:
          player.money += player.bet*1.5
          blackjack = True
      return balckjack

  def ask_numeric(self, question= ''):
    move = input(f'{question}')
    while not move.isnumeric():
      print('\nPlease enter a positive numeric output.\n')
      move = input(f'{question}')
      
    return int(move)
    
def main():
  game1 = Game()
  game1.gameV1() 
  
def test():
  game1 = Game()
  print(game1.deck)
  print()
  
  t.sleep(2)
   
  game1.player.draw_cards(game1.deck, 20)
  print(game1.deck)
  print()
  
  t.sleep(2)
  
  game1.player.draw_cards(game1.deck, 30)
  print(game1.deck)

  t.sleep(2)
  game1.player.draw_cards(game1.deck, 2)
  print(game1.deck)

def test2():
  deck = DeckOfCards() 
  #deck.shuffle(display_text=False)
  for i in range(deck.get_lenght()) :
    for i in deck.pop_cards()[0].get_image():
      print(i)
 
if __name__ == '__main__':
  main()


# BUGS/FIXES:
# 1. add insurance
# 2. show only abailable moves
# 3. add splitting option


