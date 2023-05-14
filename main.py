import pygame, sys, random
from pygame.locals import *

TILE_SIZE = 80
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FPS = 2
BASIC_FONT_SIZE = 20
CARD_SIZE = 100
BLANK = None

FPS_CLOCK = None
DISPLAY_SURFACE = None
BASIC_FONT = None
BUTTONS = None

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

def draw_image(screen, image, x, y, img_width, img_height):
    image = pygame.image.load(f"{image}")
    image = pygame.transform.scale(image, (img_width, img_height))
    screen.blit(image, (x, y))
    pygame.display.update()

def display_card(screen, card, x, y):
    global CARD_SIZE

    path = './img/Cards/'
    suit = card[1]

    if suit == 'C':
        draw_image(screen, path + 'Clubs/' + card + '.png', x, y, CARD_SIZE * 0.7, CARD_SIZE )
    elif suit == 'D':
        draw_image(screen, path + 'Diamonds/' + card + '.png', x, y, CARD_SIZE * 0.7, CARD_SIZE )
    elif suit == 'H':
        draw_image(screen, path + 'Hearts/' + card + '.png', x, y, CARD_SIZE * 0.7, CARD_SIZE )
    elif suit == 'S':
        draw_image(screen, path + 'Spades/' + card + '.png', x, y, CARD_SIZE * 0.7, CARD_SIZE )
    else:
        pass

def players_cards(cards):
    player_hand.append(cards[:2])
    cards.pop(cards[0:2])
    dealer_hand = cards[2:4]
    dealer_hand.append(cards[2:4])
    cards.pop(cards[:2])
    return player_hand, dealer_hand


def allowed_bet_height(balance, bet):
    if balance < bet:
        return False
    return True


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
    return bet + (percentage * (bet / 100))


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
    global round_running, balance
    message = preparation_round_over(player_points, dealer_hand, deck)
    win_amount = 0

    round_running = False

    if message == 'win':
        win_amount = win(bet, 100)
        balance += win_amount
        return f'win | {win_amount} {bet} {balance} | {player_hand} {dealer_hand}'
    if message == 'lost':
        win_amount = win(bet, -100)
        balance += win_amount
        return f'lost | {win_amount} {bet} {balance} | {player_hand} {dealer_hand}'
    if message == 'draw':
        win_amount = win(bet, 0)
        balance += win_amount
        return f'draw | {win_amount} {bet} {balance} | {player_hand} {dealer_hand}'

def main():
    global FPS_CLOCK, DISPLAY_SURFACE, WINDOW_WIDTH, WINDOW_HEIGHT, player_hand, dealer_hand, all_cards, balance, round_running

    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', BASIC_FONT_SIZE)
    pygame.display.set_caption('Blackjack')
    pygame.display.update()
    FPS_CLOCK.tick(FPS)

    game_ended = False


    def terminate():
        pygame.quit()
        sys.exit()

    while game_ended == False:
        pygame.display.update()
        FPS_CLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()

        player_hand = []
        dealer_hand = []
        bet = 0
        cards = shuffle_cards(all_cards.copy())
        [cards, player_hand, dealer_hand] = start_round(cards, player_hand, dealer_hand)

        round_running = True

        draw_image(DISPLAY_SURFACE, './img/Other/Background.png', 0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

        display_card(DISPLAY_SURFACE, 'KC', 0, 0)
        display_card(DISPLAY_SURFACE, 'KH', 50, 50)
        display_card(DISPLAY_SURFACE, 'KD', 100, 100)

        # print("hra zacala")

        # bet = int(input(f'balance: {balance} | place your bet: '))
        # print(player_hand)
        # balance -= bet
        # while round_running:
        #     decision = input('')
        #     if 'hit' == decision:
        #         hit(player_hand, cards)
        #         print (player_hand)

        #     if 'double' == decision:
        #         balance -= bet
        #         bet += bet
        #         hit(player_hand, cards)
        #         print (player_hand)
        #         print(round_over(calculate_value_of_cards(player_hand), dealer_hand, cards, bet))

            
        #     if 'pass' == decision:
        #         print(round_over(calculate_value_of_cards(player_hand), dealer_hand, cards, bet))

        #     if calculate_value_of_cards(player_hand) > 21:
        #         print(round_over(calculate_value_of_cards(player_hand), dealer_hand, cards, bet))

    # cards = shuffle_cards()
    # [player_hand, dealer_hand, cards] = start_round(cards, player_hand, dealer_hand)

main()
