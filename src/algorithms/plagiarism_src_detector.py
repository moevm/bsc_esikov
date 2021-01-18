from abc import ABC, abstractmethod


class PlagiarismSrcDetector(ABC):
    @abstractmethod
    def search(self, check_tokens_str):
        pass
