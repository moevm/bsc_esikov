import argparse


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True)
    parser.add_argument('-d', '--dir', required=True)
    parser.add_argument('-l', '--limit', default=60)
    parameters = parser.parse_args()
    return parameters
