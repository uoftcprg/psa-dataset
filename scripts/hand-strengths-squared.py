from argparse import ArgumentParser
from collections import defaultdict
from functools import partial
from itertools import chain, combinations, permutations
from pathlib import Path
from statistics import fmean

from pokerkit import Card, Deck, Suit

CARDS = frozenset(Deck.STANDARD)
SUITS = frozenset(Suit)


def parse_args():
    parser = ArgumentParser()

    parser.add_argument('input_path', type=Path)
    parser.add_argument('output_path', type=Path)

    return parser.parse_args()


def cards2str(cards):
    return ''.join(sorted(map(repr, cards)))


def create_lookup(input_path, output_path):
    lookup = defaultdict(dict)

    with open(input_path) as input_file, open(output_path) as output_file:
        for input_line, output_line in zip(input_file, output_file):
            assert input_line is not None
            assert output_line is not None

            raw_board_cards, *raw_hole_cards = input_line.split()

            if raw_board_cards == '-':
                raw_board_cards = ''

            board_cards = cards2str(Card.parse(raw_board_cards))

            for raw_hole_cards, raw_value in zip(
                    raw_hole_cards,
                    output_line.split(),
            ):
                assert raw_hole_cards is not None
                assert raw_value is not None

                hole_cards = cards2str(Card.parse(raw_hole_cards))
                value = float(raw_value)
                lookup[board_cards][hole_cards] = value

    return lookup


def resuit_aux(suits, card):
    if card.suit in suits:
        card = Card(card.rank, suits[card.suit])

    return card


def resuit(cards, suits):
    from_suits = tuple(suits)

    for to_suits in permutations(from_suits):
        suits = dict(zip(from_suits, to_suits))

        yield tuple(map(partial(resuit_aux, suits), cards))


def query_lookup(lookup, board_cards, hole_cards):
    cards = tuple(chain(board_cards, hole_cards))
    value = None

    for cards in resuit(cards, SUITS):
        board_cards = cards[:len(board_cards)]
        hole_cards = cards[len(board_cards):]
        key0 = cards2str(board_cards)
        key1 = cards2str(hole_cards)

        if key0 in lookup and key1 in lookup[key0]:
            value = lookup[key0][key1]

            break

    assert value is not None

    return value


def main():
    args = parse_args()
    lookup = create_lookup(args.input_path, args.output_path)
    status = True

    while status:
        try:
            s = input()
        except EOFError:
            status = False
        else:
            raw_board_cards, *raw_hole_cards = s.split()

            if raw_board_cards == '-':
                raw_board_cards = ''

            board_cards = frozenset(Card.parse(raw_board_cards))
            values = []

            for raw_hole_cards in raw_hole_cards:
                hole_cards = frozenset(Card.parse(raw_hole_cards))
                next_cards = CARDS - set(board_cards) - set(hole_cards)
                count = 1 if board_cards else 3
                next_card_combinations = combinations(next_cards, count)

                values.append(
                    fmean(
                        query_lookup(
                            lookup,
                            board_cards | set(cards),
                            hole_cards,
                        )
                        for cards in next_card_combinations
                    ),
                )

            print('\t'.join(map('{:.6f}'.format, values)))


if __name__ == '__main__':
    main()
