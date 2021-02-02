from abc import ABC, abstractmethod


class SearchAPI(ABC):
    def __init__(self, file_extension):
        self._file_extension = file_extension

    @property
    @abstractmethod
    def languages(self):
        pass

    @abstractmethod
    def _send_search_request(self, func_name, page, per_page):
        pass

    @abstractmethod
    def search(self, func_name):
        pass
