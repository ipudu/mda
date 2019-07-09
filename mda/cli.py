import argparse

from mda import util
from mda.input import Parser
from mda.analysis import Measure


def mda():
    parser = argparse.ArgumentParser(description='MDA: Analysis Tools for MD Simulations')
    parser.add_argument('input', type=str, help='input file of MDA')
    args = parser.parse_args()

    # TODO:
    util.output_welcome()

    p = Parser(args.input)
    Measure(p)

    util.output_end()

if __name__ == '__main__':
    mda()