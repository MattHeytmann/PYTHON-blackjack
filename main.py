import random
player_hand = []
dealer_hand = []
played_cards = []
player_balance = 0
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

def add_extra_card(deck):
    last_third_of_deck = deck[-15:-10]
    last_third_of_deck += ['XX']

    random.shuffle(last_third_of_deck)

    return deck[:-15] + last_third_of_deck + deck[-10:]

cards += 7 * cards

def shuffle_cards():
    random.shuffle(cards)
    add_extra_card(cards)
    return cards

# def players_cards():

#     global player_hand, dealer_hand

#     player_hand.append(cards[:2])
#     cards.pop(cards[:2])
#     dealer_hand = cards[2:4]
#     dealer_hand.append(cards[2:4])
#     cards.pop(cards[:2])
#     return player_hand, dealer_hand


def start_round(cards, player, dealer):
    player += cards[:2]
    cards.pop(0)
    cards.pop(0)

    dealer += cards[:2]
    cards.pop(0)
    cards.pop(0)

    return [player_hand, dealer_hand, cards]


def hit(hand, deck):
    hand += [deck.pop(0)]
    return hand, deck


def win(bet, percentage):
    return bet + ((percentage / bet ) * 100)

def calculate_value_of_cards(hand):
    print(hand)


def main():
    global player_hand, dealer_hand, cards

    # cards = shuffle_cards()
    [player_hand, dealer_hand, cards] = start_round(cards, player_hand, dealer_hand)

    hit(player_hand, cards)
    calculate_value_of_cards(player_hand)

main()