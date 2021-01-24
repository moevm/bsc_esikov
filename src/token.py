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

    @staticmethod
    def find_border_tokens_str_in_token_list(token_list, token_str):
        for i in range(len(token_list)):
            j = 0
            while j < len(token_str) and i + j < len(token_list) and token_list[i + j].symbol == token_str[j]:
                j += 1
            if j == len(token_str):
                return token_list[i].start, token_list[i + j - 1].end
            i += 1
        return None
