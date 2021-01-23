from src import argv_parser
from src.tokenizers.c_tokenizer import CTokenizer
from src.console.dir_scanner import DirScanner


if __name__ == "__main__":
    parameters = argv_parser.parse()
    SEARCH_FILE_NAME = parameters.file
    SEARCH_DIR = parameters.dir
    FILE_EXTENSION = "c"
    try:
        with open(SEARCH_FILE_NAME, "r", encoding="utf-8") as srcFile:
            src = srcFile.read()
            print(src)
            tokenizer = CTokenizer()
            print(tokenizer.fast_tokenize(src))
    except FileNotFoundError as e:
        print("Введённый файл не найден: " + SEARCH_FILE_NAME)
    except UnicodeDecodeError as e:
        print("Файл " + SEARCH_FILE_NAME + " не удалось прочитать - не в кодировке utf-8")
    except OSError as e:
        print("Введённый параметр не является файлом: " + SEARCH_FILE_NAME)
    scanner = DirScanner(FILE_EXTENSION)
    files = scanner.scan(SEARCH_DIR)
    print(len(files))
    for file in files:
        print(file.name)
