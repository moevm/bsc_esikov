import sys
from src import argv_parser
from src.tokenizers.c_tokenizer import CTokenizer
from src.console.dir_scanner import DirScanner
from src.algorithms.heskel import Heskel
from src.algorithms.greedy_string_tiling import GreedyStringTiling
from src.token import Token
from src.similarity import Similarity
from src.src_file import SrcFile


if __name__ == "__main__":
    parameters = argv_parser.parse()

    SEARCH_FILE_PATH = parameters.file
    SEARCH_DIR = parameters.dir
    try:
        LIMIT = int(parameters.limit)
    except ValueError as e:
        print("Введённое предельное значение не является числом: " + parameters.limit)
        sys.exit(-1)
    FILE_EXTENSION = "c"

    try:
        with open(SEARCH_FILE_PATH, "r", encoding="utf-8") as srcFile:
            search_file = SrcFile(SEARCH_FILE_PATH, SEARCH_FILE_PATH, srcFile.read())
    except FileNotFoundError as e:
        print("Введённый файл не найден: " + SEARCH_FILE_PATH)
        sys.exit(-1)
    except UnicodeDecodeError as e:
        print("Файл " + SEARCH_FILE_PATH + " не удалось прочитать - не в кодировке utf-8")
        sys.exit(-1)
    except OSError as e:
        print("Введённый параметр не является файлом: " + SEARCH_FILE_PATH)
        sys.exit(-1)

    tokenizer = CTokenizer()
    scanner = DirScanner(FILE_EXTENSION)

    search_file_tokens = tokenizer.tokenize(search_file.src)
    search_file.tokens = search_file_tokens

    heskel_algo = Heskel(tokenizer.fast_tokenize(search_file.src))
    greedy_algo = GreedyStringTiling(Token.get_tokens_str_from_token_list(search_file_tokens))

    files = scanner.scan(SEARCH_DIR)
    similarity_files = []
    print("Выполняется подсчёт процентов совпадений")
    for file in files:
        similarity_percentage = heskel_algo.search(tokenizer.fast_tokenize(file.src))
        if similarity_percentage > LIMIT and search_file.path != file.path:
            file.similarity_percentage = similarity_percentage
            similarity_files.append(file)

    similarity = []
    print("Выполняется поиск схожих фрагментов")
    for file in similarity_files:
        tokens = tokenizer.tokenize(file.src)
        file.tokens = tokens
        tokens_str = file.tokens_str
        similarity_tokens_sequence = greedy_algo.search(tokens_str)
        similarity.append(Similarity(search_file, file, similarity_tokens_sequence))

    if len(similarity) > 0:
        print("Полученный результат:")
    else:
        print("В директории не было обнаружено файлов с процентом совпадения > " + str(LIMIT))
    for sim in similarity:
        check_file_similarity_src, detected_file_similarity_src = sim.get_similarity_src()
        print("$" * 30)
        print(sim.check_file_path + ":")
        for src in check_file_similarity_src:
            print(src)
            print("-" * 30)
        print("\n")
        print(sim.detected_file_path + "  --  " + str(round(sim.similarity_percentage)) + "% сходства:")
        for src in detected_file_similarity_src:
            print(src)
            print("-" * 30)
        print("\n")
