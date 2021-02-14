import argparse


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--check', required=True)
    parser.add_argument('-d', '--data', default=SEARCH_ALL_REPOS)
    parser.add_argument('-l', '--limit', default=60)
    parser.add_argument('-b', '--branches', choices=[SEARCH_MAIN_BRANCH, SEARCH_ALL_BRANCHES], default=SEARCH_MAIN_BRANCH)
    parameters = parser.parse_args()
    return parameters


SEARCH_ALL_REPOS = 'NETWORK'
SEARCH_MAIN_BRANCH = '0'
SEARCH_ALL_BRANCHES = '1'
