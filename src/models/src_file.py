from src.models.token import Token


class SrcFile:
    def __init__(self, name, path, src):
        self.__name = name
        self.__path = path
        self.__src = src
        self.__tokens = []
        self.__similarity_percentage = 0
        self.__source = ''

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

    @property
    def similarity_percentage(self):
        return self.__similarity_percentage

    @similarity_percentage.setter
    def similarity_percentage(self, similarity_percentage):
        self.__similarity_percentage = similarity_percentage

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, source):
        self.__source = source

    @staticmethod
    def is_file_have_this_extension(path, file_extension):
        return path.split('.')[-1].lower() == file_extension
