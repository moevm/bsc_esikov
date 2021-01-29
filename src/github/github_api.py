import requests
import base64
import os
import sys
from src.src_file import SrcFile


class GithubAPI:
    def __init__(self, token, file_extension):
        self.__token = token
        self.__file_extension = file_extension

    def __send_request(self, api_url):
        address = 'https://api.github.com'
        if api_url[0] != "/":
            address += "/"
        headers = {
            'Authorization': 'token ' + self.__token
        }
        return requests.get(address + api_url, headers=headers)

    def get_name_default_branch(self, owner_login, repo_name):
        api_url = '/repos/{owner}/{repo}'.format(owner=owner_login, repo=repo_name)
        response = self.__send_request(api_url)
        return response.json()['default_branch']

    def get_sha_last_commit_in_default_branch(self, owner_login, repo_name, branch_name):
        api_url = '/repos/{owner}/{repo}/branches/{branch}'.format(owner=owner_login, repo=repo_name, branch=branch_name)
        response = self.__send_request(api_url)
        return response.json()['commit']['sha']

    def get_src_file_from_sha(self, owner_login, repo_name, sha, file_path):
        api_url = '/repos/{owner}/{repo}/git/blobs/{sha}'.format(owner=owner_login, repo=repo_name, sha=sha)
        response = self.__send_request(api_url)
        if response.json()['encoding'] == 'base64':
            print(file_path)
            file_bytes = base64.b64decode(response.json()['content'])
            src = file_bytes.decode('utf-8')
            return SrcFile(os.path.basename(file_path), file_path, src)
        else:
            print("В репозитории " + repo_name + " файл " + file_path + "закодирован не в формате base 64. " +
                  "Невозможно выполнить его декодирование")

    def get_files_set_from_sha_commit(self, owner_login, repo_name, sha, file_path='.'):
        files = set()
        api_url = '/repos/{owner}/{repo}/git/trees/{sha}'.format(owner=owner_login, repo=repo_name, sha=sha)
        response = self.__send_request(api_url)
        tree = response.json()['tree']
        for node in tree:
            current_path = file_path + "/" + node["path"]
            if node["type"] == "tree":
                files |= self.get_files_set_from_sha_commit(owner_login, repo_name, node['sha'], current_path)
            if node["type"] == "blob" and SrcFile.is_file_have_this_extension(current_path, self.__file_extension):
                files.add(self.get_src_file_from_sha(owner_login, repo_name, node["sha"], current_path))
        return files

    def get_files_list_from_default_branch(self, owner_login, repo_name):
        try:
            default_branch_name = self.get_name_default_branch(owner_login, repo_name)
            sha_last_commit = self.get_sha_last_commit_in_default_branch(owner_login, repo_name, default_branch_name)
            files_set = self.get_files_set_from_sha_commit(owner_login, repo_name, sha_last_commit)
        except KeyError as e:
            print("Github API rate limit exceeded. Try later")
            sys.exit(-1)
        return list(files_set)
