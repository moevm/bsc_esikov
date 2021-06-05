import requests
import base64
import os
from src.models.src_file import SrcFile
from src.network.url_parser import UrlParser
from src.console.argv_parser import SEARCH_ALL_BRANCHES


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
        response = requests.get(address + api_url, headers=headers, params=params, timeout=7)
        if response.status_code == 403:
            raise KeyError
        response.raise_for_status()
        return response

    def get_name_default_branch(self, owner_login, repo_name):
        api_url = '/repos/{owner}/{repo}'.format(owner=owner_login, repo=repo_name)
        response_json = self.__send_get_request(api_url).json()
        return response_json['default_branch']

    def get_sha_last_branch_commit(self, owner_login, repo_name, branch_name):
        api_url = '/repos/{owner}/{repo}/branches/{branch}'.format(owner=owner_login, repo=repo_name, branch=branch_name)
        response_json = self.__send_get_request(api_url).json()
        return response_json['commit']['sha']

    def get_src_file_from_sha(self, owner_login, repo_name, sha, file_path, branch):
        api_url = '/repos/{owner}/{repo}/git/blobs/{sha}'.format(owner=owner_login, repo=repo_name, sha=sha)
        response_json = self.__send_get_request(api_url).json()
        if response_json['encoding'] == 'base64':
            file_bytes = base64.b64decode(response_json['content'])
            try:
                src = file_bytes.decode('utf-8')
            except ValueError as e:
                src = GithubAPI.decode_error_handler(bytearray(file_bytes), e.args[2])
            file = SrcFile(os.path.basename(file_path), file_path, src)
            file.source = 'https://github.com/{owner}/{repo}/blob/{branch}/{path}'.format(owner=owner_login, repo=repo_name, branch=branch, path=file_path[2:])
            return file
        else:
            print("В репозитории " + repo_name + " файл " + file_path + "закодирован не в формате base 64. " +
                  "Невозможно выполнить его декодирование")

    @staticmethod
    def decode_error_handler(bytearray_src, position):
        try:
            bytearray_src[position] = 32
            bytearray_src = bytearray_src.decode('utf-8')
            return bytearray_src
        except ValueError as e:
            return GithubAPI.decode_error_handler(bytearray_src, e.args[2])

    def get_files_generator_from_sha_commit(self, owner_login, repo_name, sha, file_path, branch):
        api_url = '/repos/{owner}/{repo}/git/trees/{sha}'.format(owner=owner_login, repo=repo_name, sha=sha)
        response_json = self.__send_get_request(api_url).json()
        tree = response_json['tree']
        for node in tree:
            current_path = file_path + "/" + node["path"]
            if node["type"] == "tree":
                yield from self.get_files_generator_from_sha_commit(owner_login, repo_name, node['sha'], current_path, branch)
            if node["type"] == "blob" and SrcFile.is_file_have_this_extension(current_path, self.__file_extension):
                yield self.get_src_file_from_sha(owner_login, repo_name, node["sha"], current_path, branch)

    def get_list_repo_branches(self, owner_login, repo_name, default_branch=None, per_page=30):
        branches = []
        page = 1
        while True:
            api_url = '/repos/{owner}/{repo}/branches'.format(owner=owner_login, repo=repo_name)
            params = {
                "per_page": per_page,
                "page": page
            }
            response_json = self.__send_get_request(api_url, params=params).json()

            if len(response_json) == 0:
                break

            for node in response_json:
                branch_name = node["name"]
                if branch_name != default_branch:
                    branches.append(branch_name)
            page += 1

        return branches

    def get_files_generator_from_repo_url(self, repo_url, branch_policy):
        owner_login, repo_name = UrlParser.parse_github_repo(repo_url)

        # first check - main branch
        default_branch = self.get_name_default_branch(owner_login, repo_name)
        branches = [default_branch]
        if branch_policy == SEARCH_ALL_BRANCHES:
            branches += self.get_list_repo_branches(owner_login, repo_name, default_branch=default_branch)

        for branch in branches:
            sha_last_commit = self.get_sha_last_branch_commit(owner_login, repo_name, branch)
            yield from self.get_files_generator_from_sha_commit(owner_login, repo_name, sha_last_commit, ".", branch)

    def get_file_from_url(self, file_url):
        owner_login, repo_name, branch_name, path = UrlParser.parse_github_content_path(file_url)
        api_url = '/repos/{owner}/{repo}/contents/{path}'.format(owner=owner_login, repo=repo_name, path=path)
        params = {
            'ref': branch_name
        }
        response_json = self.__send_get_request(api_url, params=params).json()
        file = self.get_src_file_from_sha(owner_login, repo_name, response_json['sha'], "./" + response_json['path'], branch_name)
        file.source = file_url

        return file

    def get_files_from_dir_url(self, dir_url):
        owner_login, repo_name, branch_name, path = UrlParser.parse_github_content_path(dir_url)
        api_url = '/repos/{owner}/{repo}/contents/{path}'.format(owner=owner_login, repo=repo_name, path=path)
        params = {
            'ref': branch_name
        }
        response_json = self.__send_get_request(api_url, params=params).json()

        for node in response_json:
            current_path = "./" + node["path"]
            if node["type"] == "dir":
                yield from self.get_files_generator_from_sha_commit(owner_login, repo_name, node['sha'], current_path, branch_name)
            if node["type"] == "file" and SrcFile.is_file_have_this_extension(node["name"], self.__file_extension):
                yield self.get_src_file_from_sha(owner_login, repo_name, node["sha"], current_path, branch_name)
