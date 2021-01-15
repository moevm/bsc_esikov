class SrcFile:
    def __init__(self, name, src):
        self.__name = name
        self.__src = src

    @property
    def name(self):
        return self.__name

    @property
    def src(self):
        return self.__src
