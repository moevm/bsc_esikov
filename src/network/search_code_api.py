import requests
import sys
from src.src_file import SrcFile
from src.network.search_api import SearchAPI


class SearchCodeAPI(SearchAPI):
    def __init__(self, file_extension):
        SearchAPI.__init__(self, file_extension)

    @property
    def languages(self):
        return {
            "c": "28",
            "java": "23",
            "py": "19"
        }

    def _send_search_request(self, func_name, page, per_page=16):
        url = 'https://searchcode.com/api/codesearch_I/?q={func_name}&lan={language}&per_page={per_page}&p={p}'.format(
            func_name=func_name,
            language=self.languages[self._file_extension],
            per_page=per_page,
            p=page
        )
        return self._send_get_request(url)

    def search(self, func_name):
        try_next = True
        page = 0
        while True:
            response_json = self._send_search_request(func_name, page).json()
            if response_json['results'] is None:
                # Если в ответе вернулось null в полях, то попробовать загрузить следующую страницу
                if try_next:
                    page += 1
                    try_next = False
                    continue
                # Если 2 раза подряд в ответе вернулось null в полях, то заканчивается перебор страниц
                else:
                    break
            if len(response_json['results']) == 0:
                break
            for result in response_json['results']:
                file_name = result['filename']
                path = '.' + result['location'] + '/' + file_name
                src = self._get_src_code_file_from_id(result['id'])
                file = SrcFile(file_name, path, src)
                file.source = result['repo']
                yield file
            page += 1

    def _get_src_code_file_from_id(self, code_id):
        url = 'https://searchcode.com/api/result/{codeid}/'.format(codeid=code_id)
        return self._send_get_request(url).json()['code']

    def _send_get_request(self, url):
        response = requests.get(url, timeout=7)
        if response.status_code == 429:
            print('Лимит запросов на searchcode.com исчерпан. Попробуйте позже')
            sys.exit(-1)
        response.raise_for_status()
        return response
