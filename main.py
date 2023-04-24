import random
player_hand = []
dealer_hand = []
balance = 1000
bet = input(int)
played_cards = []
player_balance = 0
round_running = True
all_cards = [
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

def players_cards(cards):
    player_hand.append(cards[:2])
    cards.pop(cards[0:2])
    dealer_hand = cards[2:4]
    dealer_hand.append(cards[2:4])
    cards.pop(cards[:2])
    return player_hand, dealer_hand
# print (all_cards)
# played_cards = []

def allowed_bet_height(balance, bet):
    if balance < bet:
        return False
    return True

# def hit(deck, last_third_of_deck, cards): # should take another card from deck
#     player_hand.append(cards[0])
#     cards.pop(cards[0])
#     random.shuffle(last_third_of_deck)

#     return deck[:-15] + last_third_of_deck + deck[-10:], player_hand

# hit(all_cards, )

all_cards += 7 * all_cards

def shuffle_cards(deck):
    random.shuffle(deck)
    add_extra_card(deck)
    return deck

def start_round(cards, player, dealer):
    player += cards[:2]
    cards.pop(0)
    cards.pop(0)

    dealer += cards[:2]
    cards.pop(0)
    cards.pop(0)

    return [cards, player, dealer]


def hit(hand, deck):
    hand += [deck.pop(0)]
    return hand, deck


def win(bet, percentage):
    return bet + ((percentage / bet ) * 100)


def calculate_value_of_cards(hand):

    value = 0
    nums_of_a = 0

    for card in hand:
        if card[0] == 'a':
            nums_of_a += 1
        elif card[0] == 'j' or card[0] == 'k' or card[0] == 'q' or card[0] == 'x':
            value += 10
        else:
            value += int(card[0])
    
    for _ in range(nums_of_a):
        if value + 11 + (nums_of_a - 1) <= 21:
            value += 11
        else:
            value += 1
    return(value)

print(calculate_value_of_cards(['xc', 'qh', 'qh']))

def double(bet, deck):
    global player_hand
    bet = 2 * bet
    hit(player_hand, deck)
    return bet

def dealer_play(dealer_hand, deck):
    while calculate_value_of_cards(dealer_hand) < 16:
        hit(dealer_hand, deck)

    return dealer_hand

def preparation_round_over(player_points, dealer_hand, deck):
    dealer_hand = dealer_play(dealer_hand, deck)
    print('round ended')

    # hráč vyhraje pokud bude háč mít méně nebo rovno 21 a dealer bude mít v případě že má hráč méně nebo rovno 21 méně než hráč nebo více než 21
    if (player_points <= 21 and calculate_value_of_cards(dealer_hand) < player_points) or (player_points <= 21 and calculate_value_of_cards(dealer_hand) > 21):
        return 'win'
    if player_points > 21 or (calculate_value_of_cards(dealer_hand) > player_points and calculate_value_of_cards(dealer_hand) <= 21):
        return 'lost'
    if player_points == calculate_value_of_cards(dealer_hand) and player_points <= 21:
        return 'draw'
    
def round_over(player_points, dealer_hand, deck, bet):
    global round_running
    message = preparation_round_over(player_points, dealer_hand, deck)
    win_amount = 0

    round_running = False

    if message == 'win':
        win_amount = win(bet, 100)
        return f'win {win_amount} | {player_hand} {dealer_hand}'
    if message == 'lost':
        return f'lost | {player_hand} {dealer_hand}'
    if message == 'draw':
        return f'draw | {player_hand} {dealer_hand}'

def main():
    global player_hand, dealer_hand, all_cards, balance, round_running
    game_ended = False

    while game_ended == False:

        player_hand = []
        dealer_hand = []
        bet = 0
        cards = shuffle_cards(all_cards.copy())
        [cards, player_hand, dealer_hand] = start_round(cards, player_hand, dealer_hand)

        round_running = True

        print("hra zacala")

        print(player_hand)
        bet = int(input(f'balance: {balance} | place your bet: '))
        while True:
            decision = input('')
            if 'hit' == decision:
                hit(player_hand, cards)
                print (player_hand)

            if 'double' == decision:
                bet = double(bet, cards)
                print (player_hand)
                print(round_over(calculate_value_of_cards(player_hand), dealer_hand, cards, bet))

            
            if 'pass' == decision:
                print(round_over(calculate_value_of_cards(player_hand), dealer_hand, cards, bet))

            if calculate_value_of_cards(player_hand) > 21:
                print(round_over(calculate_value_of_cards(player_hand), dealer_hand, cards, bet))

    cards = shuffle_cards()
    [player_hand, dealer_hand, cards] = start_round(cards, player_hand, dealer_hand)

main()
