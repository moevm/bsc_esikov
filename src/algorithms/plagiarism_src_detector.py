from abc import ABC, abstractmethod


class PlagiarismSrcDetector(ABC):
    @abstractmethod
    def search(self, search_tokens_str):
        pass
