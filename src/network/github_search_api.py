import requests
import sys
from src.network.search_api import SearchAPI
from src.network.github_api import GithubAPI


class GithubSearchAPI(SearchAPI):
    def __init__(self, file_extension, token):
        SearchAPI.__init__(self, file_extension)
        self._token = token

    @property
    def languages(self):
        return {
            "c": "c",
            "java": "java",
            "py": "python"
        }

    def _send_search_request(self, func_name, page, per_page=50):
        url = 'https://api.github.com/search/code?q={func_name}+in:file+language:{language}&page={page}&per_page={per_page}'.format(
            func_name=func_name,
            language=self.languages[self._file_extension],
            page=page,
            per_page=per_page
        )
        headers = {
            'Authorization': 'token ' + self._token,
            'accept': 'application/vnd.github.v3+json',
        }
        try:
            response = requests.get(url, headers=headers, timeout=7)
            response.raise_for_status()
        except requests.exceptions.Timeout as e:
            print(str(e).split("'")[-2])
            sys.exit(-1)
        except requests.exceptions.ConnectionError as e:
            print(str(e))
            sys.exit(-1)
        except requests.exceptions.HTTPError as e:
            print(str(e))
            sys.exit(-1)
        return response

    def search(self, func_name):
        github = GithubAPI(self._token, self._file_extension)
        page = 1
        while True:
            response_json = self._send_search_request(func_name, page).json()
            if response_json['items'] is None or len(response_json['items']) == 0:
                break
            for item in response_json['items']:
                owner_login = item["repository"]["owner"]["login"]
                repo_name = item["repository"]["name"]
                path = "./" + item["path"]
                file = github.get_src_file_from_sha(owner_login, repo_name, item['sha'], path)
                file.source = item["repository"]["html_url"]
                yield file
            page += 1
