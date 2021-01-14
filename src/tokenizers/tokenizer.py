from abc import ABC, abstractmethod
import re


class Tokenizer(ABC):
    def tokenize(self, src):
        src_without_import = self.clear_import(src)
        src_without_comments = self.clear_comments(src_without_import)
        src_after_processing = self._process(src_without_comments)
        return src_after_processing

    @abstractmethod
    def _process(self, src):
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
