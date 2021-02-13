from abc import ABC, abstractmethod


class Tokenizer(ABC):
    def tokenize(self, src):
        src_with_replace_import = self.replace_import(src)
        src_with_replace_comments = self.replace_comments(src_with_replace_import)
        tokens = self._process(src_with_replace_comments)
        return tokens

    @abstractmethod
    def _process(self, src):
        pass

    @staticmethod
    @abstractmethod
    def replace_import(src):
        pass

    @staticmethod
    @abstractmethod
    def replace_comments(src):
        pass

    @staticmethod
    @abstractmethod
    def get_function_names(src):
        pass