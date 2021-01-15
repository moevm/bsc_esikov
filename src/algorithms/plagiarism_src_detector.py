from abc import ABC, abstractmethod


class PlagiarismSrcDetector(ABC):
    @staticmethod
    @abstractmethod
    def search(first, second):
        pass
