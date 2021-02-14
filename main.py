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
from src.console.path_parser import PathParser


def get_files_from_path(search_path):
    if PathParser.is_file(search_path):
        if UrlParser.is_url(search_path):
            yield GITHUB_API.get_file_from_url(search_path)
        else:
            yield DirScanner.read_file(search_path)
    else:  # if search_path is dir
        if UrlParser.is_url(search_path):
            if UrlParser.is_github_repo_url(search_path):
                yield from GITHUB_API.get_files_generator_from_repo_url(search_path, BRANCH_POLICY)
            else:
                yield from GITHUB_API.get_files_from_dir_url(search_path)
        else:
            yield from SCANNER.scan(search_path)


def scan_dir(comparable_file):
    if SEARCH_PATH == argv_parser.SEARCH_ALL_REPOS:
        func_names = TOKENIZER.get_function_names(comparable_file.src)
        dir_scan_generator = CodeSearcher.search_per_function_names(func_names, FILE_EXTENSION, settings['GITHUB_TOKEN'])
    else:
        dir_scan_generator = get_files_from_path(SEARCH_PATH)

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
        print("*" * 100)

        print(sim.check_file_source + " " + sim.check_file_path + ":")
        print("-" * 100)
        for src in check_file_similarity_src:
            print(src)
            print("-" * 100)

        source = sim.detected_file_source + " " + sim.detected_file_path
        print(source + "  --  " + str(round(sim.similarity_percentage)) + "% similarity:")
        print("-" * 100)

        for src in detected_file_similarity_src:
            print(src)
            print("-" * 100)
        print("\n")
    if len(similarity_list) == 0:
        print("No files were found with a match percentage > " + str(LIMIT))


if __name__ == "__main__":
    parameters = argv_parser.parse()

    FILE_EXTENSION = "c"
    if FILE_EXTENSION == "c":
        TOKENIZER = CTokenizer()
    else:
        print("No programming language specified")
        sys.exit(-1)
    CHECK_PATH = parameters.check
    if PathParser.is_file(CHECK_PATH):
        if not SrcFile.is_file_have_this_extension(CHECK_PATH, FILE_EXTENSION):
            print('The app only supports .c files')
            sys.exit(-1)
    SEARCH_PATH = parameters.data
    try:
        LIMIT = int(parameters.limit)
    except ValueError as e:
        print("The entered limit is not a number: " + parameters.limit)
        sys.exit(-1)
    BRANCH_POLICY = parameters.branches
    GITHUB_API = GithubAPI(settings['GITHUB_TOKEN'], FILE_EXTENSION)
    SCANNER = DirScanner(FILE_EXTENSION)

    for file in get_files_from_path(CHECK_PATH):
        file.tokens = TOKENIZER.tokenize(file.src)
        HESKEL_ALGO = Heskel(file.tokens_str)
        GREEDY_ALGO = GreedyStringTiling(file.tokens_str)

        similarity = []
        similarity_paths = []
        for sim in get_similarity(file):
            if sim.detected_file_path in similarity_paths:
                continue
            similarity.append(sim)
            similarity_paths.append(sim.detected_file_path)
        print_similarity_list(similarity)
        print("\n\n")
