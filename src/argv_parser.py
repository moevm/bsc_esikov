import argparse


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    # parser.add_argument('-p', '--path')
    parameters = parser.parse_args()
    return parameters
