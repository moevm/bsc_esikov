import os
from src.src_file import SrcFile


class DirScanner:
    def __init__(self, file_extension):
        self.__file_extension = file_extension

    def scan(self, path):
        files = []
        try:
            with os.scandir(path) as it:
                for entry in it:
                    if entry.is_dir() and entry.name[0] != ".":
                        files += self.scan(os.path.join(path, entry.name))
                    if entry.is_file() and entry.path.split('.')[-1].lower() == self.__file_extension:
                        try:
                            with open(entry.path, 'r', encoding="utf-8") as src_file:
                                files.append(SrcFile(entry.name, src_file.read()))
                        except UnicodeDecodeError as e:
                            print("Файл " + entry.path + " не удалось прочитать - не в кодировке utf-8")
        except FileNotFoundError as e:
            print("Введённая директория не найдена: " + path)
        except OSError as e:
            print("Синтаксическая ошибка в пути до директории: " + path)
        return files
