from abc import ABC, abstractmethod
import re


class Tokenizer(ABC):
    def fast_tokenize(self, src):
        src_without_import = self.clear_import(src)
        src_without_comments = self.clear_comments(src_without_import)
        token_string = self._fast_process(src_without_comments)
        return token_string

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

    @abstractmethod
    def _fast_process(self, src):
        pass

    @staticmethod
    @abstractmethod
    def clear_import(src):
        pass

    @staticmethod
    @abstractmethod
    def clear_comments(src):
        pass

    @staticmethod
    def clear_space(src):
        result = re.sub(r'\s', "", src)
        return result
