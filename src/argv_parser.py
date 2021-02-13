import argparse


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--check', required=True)
    parser.add_argument('-d', '--data', default=SEARCH_ALL_REPOS)
    parser.add_argument('-l', '--limit', default=60)
    parameters = parser.parse_args()
    return parameters


SEARCH_ALL_REPOS = 'NETWORK'
