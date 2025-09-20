from argparse import ArgumentParser
from functools import partial
from itertools import chain, combinations, permutations
from math import comb

from pokerkit import Card, Deck, Suit
from tqdm import tqdm

CARDS = frozenset(Deck.STANDARD)
SUITS = frozenset(Suit)


def parse_args():
    parser = ArgumentParser()

    parser.add_argument('board_card_count', type=int)
    parser.add_argument('hole_card_count', type=int)

    return parser.parse_args()


def cards2str(cards):
    return ''.join(map(repr, cards)) if cards else '-'


def resuit_aux(suits, card):
    if card.suit in suits:
        card = Card(card.rank, suits[card.suit])

    return card


def resuit(cards, suits):
    from_suits = tuple(suits)

    for to_suits in permutations(from_suits):
        suits = dict(zip(from_suits, to_suits))

        yield frozenset(map(partial(resuit_aux, suits), cards))


def get_unique_board_cards(board_card_count):
    lookup = set()

    for cards in tqdm(
            combinations(CARDS, board_card_count),
            total=comb(len(CARDS), board_card_count),
    ):
        for resuited_cards in resuit(cards, SUITS):
            if resuited_cards in lookup:
                break
        else:
            cards = frozenset(cards)

            lookup.add(cards)

            yield cards


def get_unique_hole_cards(board_cards, hole_card_count):
    suits = SUITS - frozenset(card.suit for card in board_cards)
    lookup = set()

    for cards in combinations(CARDS - board_cards, hole_card_count):
        for resuited_cards in resuit(cards, suits):
            if resuited_cards in lookup:
                break
        else:
            cards = frozenset(cards)

            lookup.add(cards)

            yield cards


def main():
    args = parse_args()
    board_card_count = args.board_card_count
    hole_card_count = args.hole_card_count

    for board_cards in get_unique_board_cards(board_card_count):
        print(
            *map(
                cards2str,
                chain(
                    (board_cards,),
                    get_unique_hole_cards(board_cards, hole_card_count),
                ),
            ),
        )


if __name__ == '__main__':
    main()
