class Token:
    def __init__(self, symbol, start, end):
        self.__symbol = symbol
        self.__start = start
        self.__end = end

    @property
    def symbol(self):
        return self.__symbol

    @property
    def start(self):
        return self.__start

    @property
    def end(self):
        return self.__end

    @staticmethod
    def get_tokens_str_from_token_list(token_list):
        token_str = ""
        for token in sorted(token_list, key=lambda tok: tok.start):
            token_str += token.symbol
        return token_str
