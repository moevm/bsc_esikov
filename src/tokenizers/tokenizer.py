from abc import ABC, abstractmethod
import re


class Tokenizer(ABC):
    @property
    @abstractmethod
    def keywords(self):
        pass

    def tokenize(self, src):
        src_without_import = self._clear_import(src)
        src_without_comments = self._clear_comments(src_without_import)
        src_after_processing = self._process(src_without_comments)
        src_without_space = src_after_processing    # Tokenizer.clear_space(src_after_processing)
        return src_without_space

    @abstractmethod
    def _process(self, src):
        pass

    @abstractmethod
    def _clear_import(self, src):
        pass

    @abstractmethod
    def _clear_special_characters(self, src):
        pass

    @abstractmethod
    def _clear_comments(self, src):
        pass

    @staticmethod
    def clear_space(src):
        result = re.sub(r'\s', "", src)
        return result
