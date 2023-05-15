
import math
import time
import pygame, sys, random
from pygame.locals import *

TILE_SIZE = 80
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900
FPS = 30
BASIC_FONT_SIZE = 20
CARD_SIZE = 300
BLANK = None

FPS_CLOCK = None
DISPLAY_SURFACE = None
BASIC_FONT = None
BUTTONS = None

player_hand = []
dealer_hand = []
balance = 1000.0
bet = 0
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

class Button:
    def __init__(self, image_path, x, y, width, height, do_function):
        self.image_path = image_path
        self.rect = pygame.Rect(x, y, width, height)
        self.handled = False
        self.do_function = do_function

    def handle_event(self):
        if pygame.mouse.get_pressed()[0] and not self.handled:
            mouse_position = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_position):
                return self.do_function()
        self.handled = pygame.mouse.get_pressed()[0]

def add_extra_card(deck):
    last_third_of_deck = deck[-15:-10]
    last_third_of_deck += ['XX']

def draw_image(screen, image, x, y, img_width, img_height):
    image = pygame.image.load(f"{image}")
    image = pygame.transform.scale(image, (img_width, img_height))
    screen.blit(image, (x, y))

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
        draw_image(screen, './img/Other/card_back.png', x, y, CARD_SIZE * 0.7, CARD_SIZE )

def display_text(font, text, x, y):
    text_surface = font.render(text, True, (0, 0, 0))
    DISPLAY_SURFACE.blit(text_surface, (x, y))

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
    while calculate_value_of_cards(dealer_hand) < 17:
        hit(dealer_hand, deck)

    return dealer_hand

def preparation_round_over(player_points, dealer_hand, deck):
    dealer_hand = dealer_play(dealer_hand, deck)

    # hráč vyhraje pokud bude háč mít méně nebo rovno 21 a dealer bude mít v případě že má hráč méně nebo rovno 21 méně než hráč nebo více než 21
    if (player_points <= 21 and calculate_value_of_cards(dealer_hand) < player_points) or (player_points <= 21 and calculate_value_of_cards(dealer_hand) > 21):
        return 'win'
    if player_points > 21 or (calculate_value_of_cards(dealer_hand) > player_points and calculate_value_of_cards(dealer_hand) <= 21):
        return 'lose'
    if player_points == calculate_value_of_cards(dealer_hand) and player_points <= 21:
        return 'push'
    
def round_over(player_points, dealer_hand, deck, bet):
    global round_running, balance
    message = preparation_round_over(player_points, dealer_hand, deck)
    win_amount = 0

    round_running = False

    return message

def main():
    global FPS_CLOCK, DISPLAY_SURFACE, WINDOW_WIDTH, WINDOW_HEIGHT, player_hand, dealer_hand, all_cards, balance, round_running, bet

    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', BASIC_FONT_SIZE)
    pygame.display.set_caption('Blackjack')
    pygame.display.update()
    FPS_CLOCK.tick(FPS)

    game_ended = False
    handled = False

    def terminate():
        pygame.quit()
        sys.exit()

    while game_ended == False:
        pygame.display.update()
        FPS_CLOCK.tick(FPS)

        round_running = True

        def btn_double():
            return 1
        def btn_hit():
            return 2
        def btn_stand():
            return 3
        def btn_chip_10():
            global balance
            balance -= 10
            return 10
        def btn_chip_20():
            global balance
            balance -= 20
            return 20
        def btn_chip_50():
            global balance
            balance -= 50
            return 50
        def btn_chip_100():
            global balance
            balance -= 100
            return 100
        def btn_chip_200():
            global balance
            balance -= 200
            return 200
        def btn_chip_500():
            global balance
            balance -= 500
            return 500
        def reset():
            global balance
            balance += bet
            return 0
        def start():
            player_turn()

        button_double = Button('./img/Other/Double.png', (WINDOW_WIDTH // 2) - 68, WINDOW_HEIGHT - 150, 130, 130, btn_double)
        button_hit = Button('./img/Other/hit.png', (WINDOW_WIDTH // 2) - 283, WINDOW_HEIGHT - 78, 203, 77, btn_hit)
        button_stand = Button('./img/Other/stand.png', (WINDOW_WIDTH / 2) + 80, WINDOW_HEIGHT - 78, 203, 77, btn_stand)

        button_chip_10 = Button('./img/Other/10.png', WINDOW_WIDTH - 270, WINDOW_HEIGHT - 250, 110, 110, btn_chip_10)
        button_chip_20 = Button('./img/Other/20.png', WINDOW_WIDTH - 150, WINDOW_HEIGHT - 250, 110, 110, btn_chip_20)
        button_chip_50 = Button('./img/Other/50.png', WINDOW_WIDTH - 270, WINDOW_HEIGHT - 370, 110, 110, btn_chip_50)
        button_chip_100 = Button('./img/Other/100.png', WINDOW_WIDTH - 150, WINDOW_HEIGHT - 370, 110, 110, btn_chip_100)
        button_chip_200 = Button('./img/Other/200.png', WINDOW_WIDTH - 270, WINDOW_HEIGHT - 490, 110, 110, btn_chip_200)
        button_chip_500 = Button('./img/Other/500.png', WINDOW_WIDTH - 150, WINDOW_HEIGHT - 490, 110, 110, btn_chip_500)

        button_reset = Button('./img/Other/reset.png', WINDOW_WIDTH - 250, WINDOW_HEIGHT - 130, 203, 77, reset)
        button_start = Button('./img/Other/Start.png', WINDOW_WIDTH - 250, WINDOW_HEIGHT - 560, 203, 77, start)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                try:
                    curr_bet = bet
                    bet = button_reset.handle_event()
                    if bet == None:
                        bet = curr_bet
                except (UnboundLocalError, TypeError):
                    pass
                try:
                    if bet > 0 and button_start.handle_event():
                        bet = 0
                except (UnboundLocalError, TypeError):
                    pass
                try:
                    if balance - 10 >= 0:
                        bet += button_chip_10.handle_event()
                except (UnboundLocalError, TypeError):
                    pass
                try:
                    if balance - 20 >= 0:
                        bet += button_chip_20.handle_event()
                except (UnboundLocalError, TypeError):
                    pass
                try:
                    if balance - 50 >= 0:
                        bet += button_chip_50.handle_event()
                except (UnboundLocalError, TypeError):
                    pass
                try:
                    if balance - 100 >= 0:
                        bet += button_chip_100.handle_event()
                except (UnboundLocalError, TypeError):
                    pass
                try:
                    if balance - 200 >= 0:
                        bet += button_chip_200.handle_event()
                except (UnboundLocalError, TypeError):
                    pass
                try:
                    if balance - 500 >= 0:
                        bet += button_chip_500.handle_event()
                except (UnboundLocalError, TypeError):
                    pass

        player_hand = []
        dealer_hand = []
        cards = shuffle_cards(all_cards.copy())
        [cards, player_hand, dealer_hand] = start_round(cards, player_hand, dealer_hand)

        

        def player_turn():
            global balance, bet

            while round_running and calculate_value_of_cards(player_hand) <= 21:

                button_double = Button('./img/Other/Double.png', (WINDOW_WIDTH // 2) - 68, WINDOW_HEIGHT - 150, 130, 130, btn_double)
                button_hit = Button('./img/Other/hit.png', (WINDOW_WIDTH // 2) - 283, WINDOW_HEIGHT - 78, 203, 77, btn_hit)
                button_stand = Button('./img/Other/stand.png', (WINDOW_WIDTH / 2) + 80, WINDOW_HEIGHT - 78, 203, 77, btn_stand)

                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                        terminate()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Check if the left mouse button was clicked
                            if button_double.handle_event() and len(player_hand) <= 2:
                                balance -= bet
                                bet = bet * 2
                                hit(player_hand, cards)
                                round_over(calculate_value_of_cards(player_hand), dealer_hand, cards, bet)
                            if button_hit.handle_event():
                                hit(player_hand, cards)
                            if button_stand.handle_event():
                                round_over(calculate_value_of_cards(player_hand), dealer_hand, cards, bet)

                for i, card in enumerate(dealer_hand):
                    card = card.upper()
                    display_card(DISPLAY_SURFACE, card, 427.01, 61.77)
                for i, card in enumerate(dealer_hand):
                    card = card.upper()
                    if i == 0:
                        display_card(DISPLAY_SURFACE, 'XX', 427.01 + (i * 60), 61.77 + (i * 30))
                    else:
                        display_card(DISPLAY_SURFACE, card, 427.01 + (i * 60), 61.77 + (i * 30))

                for i, card in enumerate(player_hand):
                    card = card.upper()
                    display_card(DISPLAY_SURFACE, card, 800.64, 391.21)
                for i, card in enumerate(player_hand):
                    card = card.upper()
                    display_card(DISPLAY_SURFACE, card, 800.64 + (i * 60), 391.21 + (i * 30))
                
                draw_image(DISPLAY_SURFACE, './img/Balls/' + str(calculate_value_of_cards(dealer_hand) - calculate_value_of_cards([dealer_hand[0]])) + '.png', 788.5, 149, 132, 132)
                draw_image(DISPLAY_SURFACE, './img/Balls/' + str(calculate_value_of_cards(player_hand)) + '.png', 406.63, 478.21, 132, 132)
                pygame.display.update()
                FPS_CLOCK.tick(FPS)
            time.sleep(1)
            
            btn_exit = True
            while btn_exit:

                
                button_exit = Button(f'./img/Other/{round_over(calculate_value_of_cards(player_hand), dealer_hand, cards, bet)}.png', 0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, btn_double)
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                        terminate()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if button_exit.handle_event():
                                btn_exit = False

                for i, card in enumerate(dealer_hand):
                    card = card.upper()
                    display_card(DISPLAY_SURFACE, card, 427.01, 61.77)
                for i, card in enumerate(dealer_hand):
                    card = card.upper()
                    display_card(DISPLAY_SURFACE, card, 427.01 + (i * 60), 61.77 + (i * 30))

                for i, card in enumerate(player_hand):
                    card = card.upper()
                    display_card(DISPLAY_SURFACE, card, 800.64, 391.21)
                for i, card in enumerate(player_hand):
                    card = card.upper()
                    display_card(DISPLAY_SURFACE, card, 800.64 + (i * 60), 391.21 + (i * 30))
                
                draw_image(DISPLAY_SURFACE, './img/Balls/' + str(calculate_value_of_cards(dealer_hand)) + '.png', 788.5, 149, 132, 132)
                draw_image(DISPLAY_SURFACE, button_exit.image_path, button_exit.rect.x, button_exit.rect.y, button_exit.rect.width, button_exit.rect.height)
                draw_image(DISPLAY_SURFACE, './img/Balls/' + str(calculate_value_of_cards(player_hand)) + '.png', 406.63, 478.21, 132, 132)
                pygame.display.update()
                FPS_CLOCK.tick(FPS)

            message = round_over(calculate_value_of_cards(player_hand), dealer_hand, cards, bet)
            if message == 'win':
                balance += win(bet, 0)
            if message == 'lose':
                balance -= win(bet, 0)
            if message == 'push':
                pass
        

        draw_image(DISPLAY_SURFACE, './img/Other/Background.png', 0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        draw_image(DISPLAY_SURFACE, './img/Other/Bar.png', 0, WINDOW_HEIGHT - 220, WINDOW_WIDTH, 220)

        draw_image(DISPLAY_SURFACE, button_double.image_path, button_double.rect.x, button_double.rect.y, button_double.rect.width, button_double.rect.height)
        draw_image(DISPLAY_SURFACE, button_hit.image_path, button_hit.rect.x, button_hit.rect.y, button_hit.rect.width, button_hit.rect.height)
        draw_image(DISPLAY_SURFACE, button_stand.image_path, button_stand.rect.x, button_stand.rect.y, button_stand.rect.width, button_stand.rect.height)
        draw_image(DISPLAY_SURFACE, button_chip_10.image_path, button_chip_10.rect.x, button_chip_10.rect.y, button_chip_10.rect.width, button_chip_10.rect.height)
        draw_image(DISPLAY_SURFACE, button_chip_20.image_path, button_chip_20.rect.x, button_chip_20.rect.y, button_chip_20.rect.width, button_chip_20.rect.height)
        draw_image(DISPLAY_SURFACE, button_chip_50.image_path, button_chip_50.rect.x, button_chip_50.rect.y, button_chip_50.rect.width, button_chip_50.rect.height)
        draw_image(DISPLAY_SURFACE, button_chip_100.image_path, button_chip_100.rect.x, button_chip_100.rect.y, button_chip_100.rect.width, button_chip_100.rect.height)
        draw_image(DISPLAY_SURFACE, button_chip_200.image_path, button_chip_200.rect.x, button_chip_200.rect.y, button_chip_200.rect.width, button_chip_200.rect.height)
        draw_image(DISPLAY_SURFACE, button_chip_500.image_path, button_chip_500.rect.x, button_chip_500.rect.y, button_chip_500.rect.width, button_chip_500.rect.height)
        if bet > 0 :
            draw_image(DISPLAY_SURFACE, button_start.image_path, button_start.rect.x, button_start.rect.y, button_start.rect.width, button_start.rect.height)
        draw_image(DISPLAY_SURFACE, button_reset.image_path, button_reset.rect.x, button_reset.rect.y, button_reset.rect.width, button_reset.rect.height)
        
        win_amount = str(math.floor(bet))

        display_text(BASIC_FONT, 'Balance: ' + str(balance) + '€', 50, WINDOW_HEIGHT - 38)
        display_text(BASIC_FONT, 'Bet:' + win_amount + '€', WINDOW_WIDTH - 280, WINDOW_HEIGHT - 38)
main()