class UrlParser:
    @staticmethod
    def is_url(url):
        if url[:8] == 'https://' or url[:7] == 'http://':
            return True
        else:
            return False

    @staticmethod
    def is_github_repo_url(url):
        substrings_url = url.split('/')
        if len(substrings_url) != 5:
            return False
        if substrings_url[1] != '':
            return False
        if substrings_url[2] != 'github.com':
            return False
        if substrings_url[0] == 'https:' or substrings_url[0] == 'http:':
            return True
        return False

    @staticmethod
    def parse_github_repo(github_repo_url):
        if UrlParser.is_github_repo_url(github_repo_url):
            substrings_url = github_repo_url.split('/')
            # [3] - owner repo
            # [4] - repo name
            return substrings_url[3], substrings_url[4]
        else:
            raise ValueError('Url to github repo does not contain "github.com"')

    @staticmethod
    def parse_github_content_path(github_content_path):
        substrings_url = github_content_path.split('/')
        if substrings_url[2] != 'github.com':
            raise ValueError('Url to github repo does not contain "github.com"')
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
            raise ValueError('Entered url is not a path to the contents of the github repo')
