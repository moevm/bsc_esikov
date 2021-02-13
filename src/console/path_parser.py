import os


class PathParser:
    @staticmethod
    def is_file(path):
        if os.path.split(path)[-1].find(".") == -1:
            return False
        else:
            return True
