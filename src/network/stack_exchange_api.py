import requests
import sys
from bs4 import BeautifulSoup
from src.network.search_api import SearchAPI
from src.src_file import SrcFile


class StackExchangeAPI(SearchAPI):
    def __init__(self, file_extension):
        SearchAPI.__init__(self, file_extension)

    @property
    def languages(self):
        return {
            "c": "c",
            "java": "java",
            "py": "python"
        }

    def _send_search_request(self, func_name, page, per_page=50):
        url = 'https://api.stackexchange.com/2.2/search/advanced?q={func_name}&answers={counst_answers}&tagged={language}&site=stackoverflow&page={page}&pagesize={pagesize}'.format(
            func_name=func_name,
            counst_answers=1,  # min count existing answers
            language=self.languages[self._file_extension],
            page=page,
            pagesize=per_page
        )
        try:
            response = requests.get(url, timeout=7)
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
        page = 1
        while True:
            response_json = self._send_search_request(func_name, page).json()
            if response_json['items'] is None or len(response_json['items']) == 0:
                break
            for item in response_json['items']:
                if item["is_answered"]:
                    if "accepted_answer_id" in item:
                        yield from self._get_file_from_answer_id(item["link"], item["accepted_answer_id"])
            page += 1

    def _get_file_from_answer_id(self, url, answer_id):
        response = requests.get(url, timeout=7)
        response.raise_for_status()
        if hasattr(response, "text"):
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            accepted_answer = soup.find("div", id="answer-" + str(answer_id))
            if accepted_answer is not None:
                pre_code_tags = accepted_answer.find_all("pre")
                for i in pre_code_tags:
                    code = i.find("code")
                    if code is not None:
                        file = SrcFile('Answer #' + str(answer_id), 'Answer #' + str(answer_id), code.text)
                        file.source = url
                        yield file
