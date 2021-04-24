import sys
from settings import settings
from src.console import argv_parser
from src.tokenizers.c_tokenizer import CTokenizer
from src.console.dir_scanner import DirScanner
from src.algorithms.heskel import Heskel
from src.algorithms.greedy_string_tiling import GreedyStringTiling
from src.models.similarity import Similarity
from src.models.src_file import SrcFile
from src.network.github_api import GithubAPI
from src.network.url_parser import UrlParser
from src.network.code_searcher import CodeSearcher
from src.console.path_parser import PathParser
from src.console.argv_parser import SEARCH_ALL_REPOS


class Searcher:
    def __init__(self, check_path, search_path, limit, branches, file_extension):
        if file_extension == "c":
            self._tokenizer = CTokenizer()
        else:
            print("No programming language specified")
            sys.exit(-1)
        self._github_api = GithubAPI(settings['GITHUB_TOKEN'], file_extension)
        self._dir_scanner = DirScanner(file_extension)
        self._file_extension = file_extension

        if PathParser.is_file(check_path):
            if not SrcFile.is_file_have_this_extension(check_path, file_extension):
                print('The app only supports .c files')
                sys.exit(-1)
        self._check_path = check_path
        if search_path == '':
            self._search_path = SEARCH_ALL_REPOS
        else:
            self._search_path = search_path

        self._branch_policy = branches

        try:
            self._limit = int(limit)
        except ValueError as e:
            print("The entered limit is not a number: " + limit)
            sys.exit(-1)

        self._similarity_list = []

    @property
    def similarity_list(self):
        return self._similarity_list

    def get_similarity(self, at):
        index = int(at)
        if len(self._similarity_list) == 0:
            return None
        if index >= len(self._similarity_list):
            return self._similarity_list[-1]
        if index < 0:
            return self._similarity_list[0]
        return self._similarity_list[index]

    def search_similarity(self):
        total_similarity = []
        for file in self._get_files_from_path(self._check_path):
            file.tokens = self._tokenizer.tokenize(file.src)
            heskel_algo = Heskel(file.tokens_str)
            greedy_algo = GreedyStringTiling(file.tokens_str)

            similarity = []
            similarity_paths = []
            for sim in self._get_similarity(file, greedy_algo, heskel_algo):
                if sim.detected_file_path in similarity_paths:
                    continue
                similarity.append(sim)
                similarity_paths.append(sim.detected_file_path)
            total_similarity += similarity

        self._similarity_list = total_similarity
        return total_similarity

    def _get_files_from_path(self, path):
        if PathParser.is_file(path):
            if UrlParser.is_url(path):
                yield self._github_api.get_file_from_url(path)
            else:
                yield DirScanner.read_file(path)
        else:  # if search_path is dir
            if UrlParser.is_url(path):
                if UrlParser.is_github_repo_url(path):
                    yield from self._github_api.get_files_generator_from_repo_url(path, self._branch_policy)
                else:
                    yield from self._github_api.get_files_from_dir_url(path)
            else:
                yield from self._dir_scanner.scan(path)

    def _scan_dir(self, comparable_file, heskel_algo):
        if self._search_path == argv_parser.SEARCH_ALL_REPOS:
            func_names = self._tokenizer.get_function_names(comparable_file.src)
            dir_scan_generator = CodeSearcher.search_per_function_names(func_names, self._file_extension, settings['GITHUB_TOKEN'])
        else:
            dir_scan_generator = self._get_files_from_path(self._search_path)

        for file in dir_scan_generator:
            file.tokens = self._tokenizer.tokenize(file.src)
            # print(file.path + " : " + file.tokens_str)
            similarity_percentage = heskel_algo.search(file.tokens_str)
            if similarity_percentage > self._limit and comparable_file.path != file.path:
                file.similarity_percentage = similarity_percentage
                yield file

    def _get_similarity(self, comparable_file, greedy_algo, heskel_algo):
        for file in self._scan_dir(comparable_file, heskel_algo):
            similarity_tokens_sequence = greedy_algo.search(file.tokens_str)
            yield Similarity(comparable_file, file, similarity_tokens_sequence)

    def print_similarity_list(self):
        for sim in self._similarity_list:
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
        if len(self._similarity_list) == 0:
            print("No files were found with a match percentage > " + str(self._limit))


if __name__ == "__main__":
    parameters = argv_parser.parse()

    searcher = Searcher(
        check_path=parameters.check,
        search_path=parameters.data,
        limit=parameters.limit,
        branches=parameters.branches,
        file_extension="c"
    )

    searcher.search_similarity()
    searcher.print_similarity_list()
