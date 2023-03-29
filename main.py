import random
player_hand = []
dealer_hand = []
balance = 1000
bet = input(int)
cards = [
    '2h',
    '3h',
    '4h',
    '5h',
    '6h',
    '7h',
    '8h',
    '9h',
    'xh',
    'jh',
    'qh',
    'kh',
    'ah',
    '2c',
    '3c',
    '4c',
    '5c',
    '6c',
    '7c',
    '8c',
    '9c',
    'xc',
    'jc',
    'qc',
    'kc',
    'ac',
    '2s',
    '3s',
    '4s',
    '5s',
    '6s',
    '7s',
    '8s',
    '9s',
    'xs',
    'js',
    'qs',
    'ks',
    'as',
    '2d',
    '3d',
    '4d',
    '5d',
    '6d',
    '7d',
    '8d',
    '9d',
    'xd',
    'jd',
    'qd',
    'kd',
    'ad',
]
cards += 7 * cards

def shuffle_cards():
    random.shuffle(cards)
    return cards
print (shuffle_cards())

def players_cards():
    player_hand.append(cards[:2])
    cards.pop(cards[0:2])
    dealer_hand = cards[2:4]
    dealer_hand.append(cards[2:4])
    cards.pop(cards[:2])
    return player_hand, dealer_hand
print (players_cards())

# played_cards = []

def allowed_bet_height(balance, bet):
    if balance < bet:
        return False
    return True

def hit(): # should take another card from deck
    player_hand.append(cards[0])
    cards.pop(cards[0])
    return player_hand