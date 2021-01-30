class UrlParser:
    @staticmethod
    def is_url(url):
        if url[:8] == 'https://' or url[:7] == 'http://':
            return True
        else:
            return False

    @staticmethod
    def parse_github_repo(github_repo_url):
        return UrlParser.__github_parse(github_repo_url, UrlParser.__github_repo_return_func)

    @staticmethod
    def __github_repo_return_func(substrings_url):
        # [3] - owner repo
        # [4] - repo name
        return substrings_url[3], substrings_url[4]

    @staticmethod
    def parse_github_file_path(github_file_path):
        return UrlParser.__github_parse(github_file_path, UrlParser.__github_file_path_return_func)

    @staticmethod
    def __github_file_path_return_func(substrings_url):
        file_path = ""
        # [7] - begin file path in repo
        for i in range(7, len(substrings_url)):
            file_path += substrings_url[i] + "/"
        file_path = file_path[:-1]  # delete last "/"
        # [5] - object type: blob, tree...
        if substrings_url[5] != 'blob':
            raise ValueError('Переданный путь не является путём до файла в github репозитории')
        # [3] - owner repo
        # [4] - repo name
        # [6] - branch name
        return substrings_url[3], substrings_url[4], substrings_url[6], file_path

    @staticmethod
    def __github_parse(path, return_func):
        substrings_url = path.split('/')
        if substrings_url[2] == 'github.com':
            return return_func(substrings_url)
        else:
            raise ValueError('Url к github репозиторию не содержит "github.com"')
