class SrcFile:
    def __init__(self, name, path, src):
        self.__name = name
        self.__path = path
        self.__src = src

    @property
    def name(self):
        return self.__name

    @property
    def path(self):
        return self.__path

    @property
    def src(self):
        return self.__src
