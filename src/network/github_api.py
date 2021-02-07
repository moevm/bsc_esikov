import requests
import base64
import os
import sys
from src.src_file import SrcFile
from src.network.url_parser import UrlParser


class GithubAPI:
    def __init__(self, token, file_extension):
        self.__token = token
        self.__file_extension = file_extension

    def __send_get_request(self, api_url, headers={}, params={}):
        address = 'https://api.github.com'
        if api_url[0] != "/":
            address += "/"
        headers.update({
            'Authorization': 'token ' + self.__token,
            'accept': 'application/vnd.github.v3+json',
        })
        try:
            response = requests.get(address + api_url, headers=headers, params=params, timeout=7)
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
        except KeyError as e:
            # 5000 requests per hour
            # api_url = 'rate_limit' - for check count available requests
            print("Github API rate limit exceeded. Limit = 5000 requests per hour. Try later")
            sys.exit(-1)
        return response

    def get_name_default_branch(self, owner_login, repo_name):
        api_url = '/repos/{owner}/{repo}'.format(owner=owner_login, repo=repo_name)
        response_json = self.__send_get_request(api_url).json()
        return response_json['default_branch']

    def get_sha_last_commit_in_default_branch(self, owner_login, repo_name, branch_name):
        api_url = '/repos/{owner}/{repo}/branches/{branch}'.format(owner=owner_login, repo=repo_name, branch=branch_name)
        response_json = self.__send_get_request(api_url).json()
        return response_json['commit']['sha']

    def get_src_file_from_sha(self, owner_login, repo_name, sha, file_path):
        api_url = '/repos/{owner}/{repo}/git/blobs/{sha}'.format(owner=owner_login, repo=repo_name, sha=sha)
        response_json = self.__send_get_request(api_url).json()
        if response_json['encoding'] == 'base64':
            file_bytes = base64.b64decode(response_json['content'])
            src = file_bytes.decode('utf-8')
            return SrcFile(os.path.basename(file_path), file_path, src)
        else:
            print("В репозитории " + repo_name + " файл " + file_path + "закодирован не в формате base 64. " +
                  "Невозможно выполнить его декодирование")

    def get_files_generator_from_sha_commit(self, owner_login, repo_name, sha, file_path='.'):
        api_url = '/repos/{owner}/{repo}/git/trees/{sha}'.format(owner=owner_login, repo=repo_name, sha=sha)
        response_json = self.__send_get_request(api_url).json()
        tree = response_json['tree']
        for node in tree:
            current_path = file_path + "/" + node["path"]
            if node["type"] == "tree":
                yield from self.get_files_generator_from_sha_commit(owner_login, repo_name, node['sha'], current_path)
            if node["type"] == "blob" and SrcFile.is_file_have_this_extension(current_path, self.__file_extension):
                yield self.get_src_file_from_sha(owner_login, repo_name, node["sha"], current_path)

    def get_files_generator_from_repo_url(self, repo_url):
        try:
            owner_login, repo_name = UrlParser.parse_github_repo(repo_url)
        except ValueError as e:
            print(str(e))
            sys.exit(-1)

        default_branch_name = self.get_name_default_branch(owner_login, repo_name)
        sha_last_commit = self.get_sha_last_commit_in_default_branch(owner_login, repo_name, default_branch_name)
        files_generator = self.get_files_generator_from_sha_commit(owner_login, repo_name, sha_last_commit)

        return files_generator

    def get_file_from_url(self, file_url):
        try:
            owner_login, repo_name, branch_name, path = UrlParser.parse_github_file_path(file_url)
        except ValueError as e:
            print(str(e))
            sys.exit(-1)

        api_url = '/repos/{owner}/{repo}/contents/{path}'.format(owner=owner_login, repo=repo_name, path=path)
        params = {
            'ref': branch_name
        }
        response_json = self.__send_get_request(api_url, params=params).json()
        file = self.get_src_file_from_sha(owner_login, repo_name, response_json['sha'], "./" + path)

        return file
