import sys
import argparse

from mda import util
from mda.log import Logger
from mda.paper import Paper
from mda.input import Parser
from mda.analysis import Measure


def mda():
    parser = argparse.ArgumentParser(
        description="MDA: Analysis Tools for MD Simulations"
    )
    parser.add_argument("input", type=str, help="input file of MDA")
    args = parser.parse_args()

    # TODO:
    sys.stdout = Logger()
    start = util.output_welcome()

    paper = Paper(args.input)

    if not paper.flag:

        p = Parser(args.input)
        Measure(p)

    util.output_end(start)


if __name__ == "__main__":
    mda()
