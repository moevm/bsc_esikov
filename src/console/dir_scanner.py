import os
import sys
from src.models.src_file import SrcFile


class DirScanner:
    def __init__(self, file_extension):
        self.__file_extension = file_extension

    def scan(self, path):
        try:
            with os.scandir(path) as it:
                for entry in it:
                    if entry.is_dir() and entry.name[0] != ".":
                        yield from self.scan(os.path.join(path, entry.name))
                    if entry.is_file() and SrcFile.is_file_have_this_extension(entry.path, self.__file_extension):
                        try:
                            with open(entry.path, 'r', encoding="utf-8") as src_file:
                                yield SrcFile(entry.name, entry.path, src_file.read())
                        except UnicodeDecodeError as e:
                            print(e)
                            print("File " + entry.path + " could not be read - not encoded utf-8")
        except (FileNotFoundError, OSError) as e:
            print(e)
            sys.exit(-1)

    @staticmethod
    def read_file(path):
        try:
            with open(path, "r", encoding="utf-8") as src_file:
                return SrcFile(path, path, src_file.read())
        except (FileNotFoundError, OSError) as e:
            print(e)
            sys.exit(-1)
        except UnicodeDecodeError as e:
            print(e)
            print("File " + path + " could not be read - not encoded utf-8")
            sys.exit(-1)
