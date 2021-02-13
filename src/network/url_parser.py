class UrlParser:
    @staticmethod
    def is_url(url):
        if url[:8] == 'https://' or url[:7] == 'http://':
            return True
        else:
            return False

    @staticmethod
    def parse_github_repo(github_repo_url):
        substrings_url = github_repo_url.split('/')
        if substrings_url[2] == 'github.com':
            # [3] - owner repo
            # [4] - repo name
            return substrings_url[3], substrings_url[4]
        else:
            raise ValueError('Url к github репозиторию не содержит "github.com"')

    @staticmethod
    def parse_github_content_path(github_content_path):
        substrings_url = github_content_path.split('/')
        if substrings_url[2] != 'github.com':
            raise ValueError('Url к github репозиторию не содержит "github.com"')
        path = ""
        # [7] - begin content path in repo
        for i in range(7, len(substrings_url)):
            path += substrings_url[i] + "/"
        path = path[:-1]  # delete last "/"
        # [5] - object type: blob, tree...
        if substrings_url[5] == 'blob' or substrings_url[5] == 'tree':
            # [3] - owner repo
            # [4] - repo name
            # [6] - branch name
            return substrings_url[3], substrings_url[4], substrings_url[6], path
        else:
            raise ValueError('Переданный url не является путём до содержимого github репозитория')
