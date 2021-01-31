import requests
import sys
from src.src_file import SrcFile


class SearchCodeAPI:
    LANGUAGE = {
        "c": 28,
        "java": 23,
        "py": 19
    }

    @staticmethod
    def __send_get_request(api_url):
        address = 'https://searchcode.com/api'
        if api_url[0] != "/":
            address += "/"
        response = requests.get(address + api_url, timeout=7)
        if response.status_code == 429:
            print('Лимит запросов на searchcode.com исчерпан. Попробуйте позже')
            sys.exit(-1)
        response.raise_for_status()
        return response

    @staticmethod
    def get_files_generator_from_list_func_names(list_func_names, file_extension, per_page=16):
        for func_name in list_func_names:
            p = 0
            try_next = True
            while True:
                api_url = '/codesearch_I/?q=' + func_name + '&lan=' + str(SearchCodeAPI.LANGUAGE[file_extension])\
                          + '&per_page=' + str(per_page) + '&p=' + str(p)
                response_json = SearchCodeAPI.__send_get_request(api_url).json()
                if response_json['results'] is None:
                    # Если в ответе вернулось null в полях, то попробовать загрузить следующую страницу
                    if try_next:
                        p += 1
                        try_next = False
                        continue
                    # Если 2 раза подряд в ответе вернулось null в полях, то заканчивается перебор страниц
                    else:
                        break
                if len(response_json['results']) == 0:
                    break
                for result in response_json['results']:
                    file_response = SearchCodeAPI.__send_get_request('/result/' + str(result['id'])).json()
                    file_name = result['filename']
                    path = '.' + result['location'] + '/' + file_name
                    file = SrcFile(file_name, path, file_response['code'])
                    file.source = result['repo']
                    yield file
                p += 1
