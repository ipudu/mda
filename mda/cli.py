import argparse
import util

from input import Parser
from analysis import Measure


def mda():
    parser = argparse.ArgumentParser(description='mda: analysis tools for MD simulations')
    parser.add_argument('input', type=str, help='input file of mda')
    args = parser.parse_args()

    # TODO:
    util.output_welcome()

    p = Parser(args.input)
    Measure(p)

    util.output_end()

if __name__ == '__main__':
    mda()