import sys
from settings import settings
from src import argv_parser
from src.tokenizers.c_tokenizer import CTokenizer
from src.console.dir_scanner import DirScanner
from src.algorithms.heskel import Heskel
from src.algorithms.greedy_string_tiling import GreedyStringTiling
from src.token import Token
from src.similarity import Similarity
from src.src_file import SrcFile
from src.network.github_api import GithubAPI
from src.network.url_parser import UrlParser


def get_search_file():
    if UrlParser.is_url(SEARCH_FILE_PATH):
        return GITHUB_API.get_file_from_url(SEARCH_FILE_PATH)
    else:
        return DirScanner.read_file(SEARCH_FILE_PATH)


def scan_dir(comparable_file):
    if UrlParser.is_url(SEARCH_DIR):
        dir_scanner = GITHUB_API.get_files_generator_from_repo_url
    else:
        dir_scanner = SCANNER.scan

    for file in dir_scanner(SEARCH_DIR):
        similarity_percentage = HESKEL_ALGO.search(TOKENIZER.fast_tokenize(file.src))
        if similarity_percentage > LIMIT and comparable_file.path != file.path:
            file.similarity_percentage = similarity_percentage
            yield file


def get_similarity(comparable_file):
    for file in scan_dir(comparable_file):
        file.tokens = TOKENIZER.tokenize(file.src)
        similarity_tokens_sequence = GREEDY_ALGO.search(file.tokens_str)
        yield Similarity(comparable_file, file, similarity_tokens_sequence)


if __name__ == "__main__":
    parameters = argv_parser.parse()

    FILE_EXTENSION = "c"
    SEARCH_FILE_PATH = parameters.file
    if not SrcFile.is_file_have_this_extension(SEARCH_FILE_PATH, FILE_EXTENSION):
        print('Приложение поддерживает только файлы с расширением .c')
        sys.exit(-1)
    SEARCH_DIR = parameters.dir
    try:
        LIMIT = int(parameters.limit)
    except ValueError as e:
        print("Введённое предельное значение не является числом: " + parameters.limit)
        sys.exit(-1)
    GITHUB_API = GithubAPI(settings['GITHUB_TOKEN'], FILE_EXTENSION)
    SCANNER = DirScanner(FILE_EXTENSION)
    TOKENIZER = CTokenizer()

    search_file = get_search_file()
    HESKEL_ALGO = Heskel(TOKENIZER.fast_tokenize(search_file.src))
    search_file.tokens = TOKENIZER.tokenize(search_file.src)
    GREEDY_ALGO = GreedyStringTiling(Token.get_tokens_str_from_token_list(search_file.tokens))

    is_find_similarity = False
    for sim in get_similarity(search_file):
        check_file_similarity_src, detected_file_similarity_src = sim.get_similarity_src()
        print("*" * 60)
        print(sim.check_file_path + ":")
        print("-" * 60)
        for src in check_file_similarity_src:
            print(src)
            print("-" * 60)
        print(sim.detected_file_path + "  --  " + str(round(sim.similarity_percentage)) + "% сходства:")
        print("-" * 60)
        for src in detected_file_similarity_src:
            print(src)
            print("-" * 60)
        print("\n")
        is_find_similarity = True
    if is_find_similarity is False:
        print("В директории не было обнаружено файлов с процентом совпадения > " + str(LIMIT))
