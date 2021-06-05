from src.network.github_search_api import GithubSearchAPI
from src.network.search_code_api import SearchCodeAPI
from src.network.stack_exchange_api import StackExchangeAPI


class CodeSearcher:
    @staticmethod
    def search_per_function_names(list_func_names, file_extension, github_token):
        search_api = [
            # SearchCodeAPI(file_extension),
            GithubSearchAPI(file_extension, github_token),
            StackExchangeAPI(file_extension)
        ]

        for func_name in list_func_names:
            for api in search_api:
                yield from api.search(func_name)
