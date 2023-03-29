from math import floor
import random

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

    print(last_third_of_deck)
    print(deck[:-15], "--------")
    print(deck[-10:], "********")

    last_third_of_deck += ['XX']

    random.shuffle(last_third_of_deck)

    return deck[:-15] + last_third_of_deck + deck[-10:]

print(len(add_extra_card(cards)))

cards += 7 * cards

def shuffle_cards():
    random.shuffle(cards)
    return cards
