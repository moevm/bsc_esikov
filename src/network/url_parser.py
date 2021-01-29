class UrlParser:
    @staticmethod
    def parse_github_repo(github_repo_url):
        substrings_url = github_repo_url.split('/')
        if substrings_url[2] == 'github.com':
            return substrings_url[3], substrings_url[4]
        else:
            raise ValueError('Url к github репозиторию не содержит "github.com"')
