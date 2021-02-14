import time
from src.tokenizers.c_tokenizer import CTokenizer
from src.console.dir_scanner import DirScanner
from src.algorithms.heskel import Heskel
from src.algorithms.greedy_string_tiling import GreedyStringTiling
from src.token import Token


def test_c_file(path_file, count_string):
    search_file = DirScanner.read_file(path_file)
    print("-" * 150 + '\n')
    print("File of " + str(count_string) + " lines of code:\n")

    start_time = time.time()
    search_file.tokens = TOKENIZER.tokenize(search_file.src)
    print("Tokenize: %s seconds" % (time.time() - start_time))

    heskel_algo = Heskel(search_file.tokens_str)
    greedy_algo = GreedyStringTiling(search_file.tokens_str)

    files = []
    for file in SCANNER.scan('./examples/c/big_files'):
        files.append(file)

    token_str = []

    start_time = time.time()
    for file in files:
        token_str.append(Token.get_tokens_str_from_token_list(TOKENIZER.tokenize(file.src)))
    print("Tokenize 10 files of 1000 lines of code: %s seconds" % (time.time() - start_time))

    start_time = time.time()
    for tokens in token_str:
        heskel_algo.search(tokens)
    print("Heskel algo: %s seconds" % (time.time() - start_time))

    print("\nGreedy string tiling algo:")
    start_time = time.time()
    for tokens in token_str:
        print('Token string lengths: ' + str(len(tokens)) + ' and ' + str(len(search_file.tokens_str)))
        algo_time = time.time()
        greedy_algo.search(tokens)
        print("Greedy string tiling algo for these token strings: %s seconds" % (time.time() - algo_time))
    print("\nGreedy string tiling algo total: %s seconds" % (time.time() - start_time))

    print("\n")


if __name__ == '__main__':
    TOKENIZER = CTokenizer()
    FILE_EXTENSION = 'c'
    SCANNER = DirScanner(FILE_EXTENSION)

    test_c_file('./examples/c/100string.c', 100)
    test_c_file('./examples/c/1000string.c', 1000)
    test_c_file('./examples/c/10000string.c', 10000)
