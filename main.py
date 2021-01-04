from src import argv_parser
from src.tokenizers.c_tokenizer import CTokenizer


if __name__ == "__main__":
    parameters = argv_parser.parse()
    # print(parameters.path)
    try:
        with open(parameters.path, "r") as srcFile:
            src = srcFile.read()
            print(src)
            tokenizer = CTokenizer()
            print(tokenizer.tokenize(src))
    except Exception as e:
        print("Файл не удалось открыть")
