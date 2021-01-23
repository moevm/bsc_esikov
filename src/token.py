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
