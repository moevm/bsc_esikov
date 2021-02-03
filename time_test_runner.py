import time
from src.tokenizers.c_tokenizer import CTokenizer
from src.console.dir_scanner import DirScanner
from src.algorithms.heskel import Heskel
from src.algorithms.greedy_string_tiling import GreedyStringTiling
from src.token import Token


def test_c_file(path_file, count_string):
    search_file = DirScanner.read_file(path_file)
    print("-" * 100 + '\n')
    print("Файл из " + str(count_string) + " строк кода:\n")

    start_time = time.time()
    heskel_algo = Heskel(TOKENIZER.fast_tokenize(search_file.src))
    print("Быстрая токенизация: %s секунд" % (time.time() - start_time))

    start_time = time.time()
    search_file.tokens = TOKENIZER.tokenize(search_file.src)
    print("Обычная токенизация: %s секунд" % (time.time() - start_time))

    greedy_algo = GreedyStringTiling(Token.get_tokens_str_from_token_list(search_file.tokens))

    files = []
    for file in SCANNER.scan('./examples/c/big_files'):
        files.append(file)

    token_str = []

    start_time = time.time()
    for file in files:
        token_str.append(TOKENIZER.fast_tokenize(file.src))
    print("Быстрая токенизация 10 файлов из 1000 строк: %s секунд" % (time.time() - start_time))

    start_time = time.time()
    for tokens in token_str:
        heskel_algo.search(tokens)
    print("Алгоритм Хескела: %s секунд" % (time.time() - start_time))

    token_str = []

    start_time = time.time()
    for file in files:
        token_str.append(Token.get_tokens_str_from_token_list(TOKENIZER.tokenize(file.src)))
    print("Обычная токенизация 10 файлов из 1000 строк: %s секунд" % (time.time() - start_time))

    print("\nАлгоритм жадного строкового замощения:")
    start_time = time.time()
    for tokens in token_str:
        print('Длины строк токенов: ' + str(len(tokens)) + ' и ' + str(len(search_file.tokens_str)))
        algo_time = time.time()
        greedy_algo.search(tokens)
        print("Алгоритм жадного строкового замощения для этих строк токенов: %s секунд" % (time.time() - algo_time))
    print("\nАлгоритм жадного строкового замощения всего: %s секунд" % (time.time() - start_time))

    print("\n")


if __name__ == '__main__':
    TOKENIZER = CTokenizer()
    FILE_EXTENSION = 'c'
    SCANNER = DirScanner(FILE_EXTENSION)

    test_c_file('./examples/c/100string.c', 100)
    test_c_file('./examples/c/1000string.c', 1000)
    #test_c_file('./examples/c/10000string.c', 10000)
    big_file = DirScanner.read_file('./examples/c/10000string.c')
    start_time = time.time()
    big_file.tokens = TOKENIZER.tokenize(big_file.src)
    print("Обычная токенизация файла в 10000 строк: %s секунд" % (time.time() - start_time))
