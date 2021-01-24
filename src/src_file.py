from src.token import Token


class SrcFile:
    def __init__(self, name, path, src):
        self.__name = name
        self.__path = path
        self.__src = src
        self.__tokens = []

    @property
    def name(self):
        return self.__name

    @property
    def path(self):
        return self.__path

    @property
    def src(self):
        return self.__src

    @property
    def tokens(self):
        return self.__tokens

    @tokens.setter
    def tokens(self, tokens):
        self.__tokens = tokens

    @property
    def tokens_str(self):
        return Token.get_tokens_str_from_token_list(self.__tokens)
