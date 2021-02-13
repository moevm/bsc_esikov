import sys
from settings import settings
from src import argv_parser
from src.tokenizers.c_tokenizer import CTokenizer
from src.console.dir_scanner import DirScanner
from src.algorithms.heskel import Heskel
from src.algorithms.greedy_string_tiling import GreedyStringTiling
from src.similarity import Similarity
from src.src_file import SrcFile
from src.network.github_api import GithubAPI
from src.network.url_parser import UrlParser
from src.network.code_searcher import CodeSearcher


def get_search_file():
    if UrlParser.is_url(SEARCH_FILE_PATH):
        return GITHUB_API.get_file_from_url(SEARCH_FILE_PATH)
    else:
        return DirScanner.read_file(SEARCH_FILE_PATH)


def scan_dir(comparable_file):
    if SEARCH_DIR == argv_parser.SEARCH_ALL_REPOS:
        func_names = TOKENIZER.get_function_names(comparable_file.src)
        dir_scan_generator = CodeSearcher.search_per_function_names(func_names, FILE_EXTENSION, settings['GITHUB_TOKEN'])
    else:
        if UrlParser.is_url(SEARCH_DIR):
            dir_scan_generator = GITHUB_API.get_files_generator_from_repo_url(SEARCH_DIR)
        else:
            dir_scan_generator = SCANNER.scan(SEARCH_DIR)

    for file in dir_scan_generator:
        file.tokens = TOKENIZER.tokenize(file.src)
        similarity_percentage = HESKEL_ALGO.search(file.tokens_str)
        if similarity_percentage > LIMIT and comparable_file.path != file.path:
            file.similarity_percentage = similarity_percentage
            yield file


def get_similarity(comparable_file):
    for file in scan_dir(comparable_file):
        similarity_tokens_sequence = GREEDY_ALGO.search(file.tokens_str)
        yield Similarity(comparable_file, file, similarity_tokens_sequence)


def print_similarity_list(similarity_list):
    for sim in similarity_list:
        check_file_similarity_src, detected_file_similarity_src = sim.get_similarity_src()
        print("*" * 60)
        print(sim.check_file_path + ":")
        print("-" * 60)
        for src in check_file_similarity_src:
            print(src)
            print("-" * 60)

        if SEARCH_DIR == argv_parser.SEARCH_ALL_REPOS:
            source = sim.source_similarity + " " + sim.detected_file_path
        else:
            source = sim.detected_file_path
        print(source + "  --  " + str(round(sim.similarity_percentage)) + "% сходства:")
        print("-" * 60)

        for src in detected_file_similarity_src:
            print(src)
            print("-" * 60)
        print("\n")
    if len(similarity_list) == 0:
        print("Не было обнаружено файлов с процентом совпадения > " + str(LIMIT))


if __name__ == "__main__":
    parameters = argv_parser.parse()

    FILE_EXTENSION = "c"
    if FILE_EXTENSION == "c":
        TOKENIZER = CTokenizer()
    else:
        print("Не указан язык программирования")
        sys.exit(-1)
    SEARCH_FILE_PATH = parameters.file
    if not SrcFile.is_file_have_this_extension(SEARCH_FILE_PATH, FILE_EXTENSION):
        print('Приложение поддерживает только файлы с расширением .c')
        sys.exit(-1)
    SEARCH_DIR = parameters.data
    try:
        LIMIT = int(parameters.limit)
    except ValueError as e:
        print("Введённое предельное значение не является числом: " + parameters.limit)
        sys.exit(-1)
    GITHUB_API = GithubAPI(settings['GITHUB_TOKEN'], FILE_EXTENSION)
    SCANNER = DirScanner(FILE_EXTENSION)

    search_file = get_search_file()
    search_file.tokens = TOKENIZER.tokenize(search_file.src)
    HESKEL_ALGO = Heskel(search_file.tokens_str)
    GREEDY_ALGO = GreedyStringTiling(search_file.tokens_str)

    similarity = []
    for sim in get_similarity(search_file):
        similarity.append(sim)
    print_similarity_list(similarity)
