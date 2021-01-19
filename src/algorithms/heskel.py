from src.algorithms.plagiarism_src_detector import PlagiarismSrcDetector


class Heskel(PlagiarismSrcDetector):
    def __init__(self, token_str):
        self.__token_str = token_str
        self.__length_n_gramm = 2
        self.__n_gramms = self.split_into_n_gramms(self.__token_str, self.__length_n_gramm)

    def search(self, search_tokens_str):
        check_str_n_gramms = self.split_into_n_gramms(search_tokens_str, self.__length_n_gramm)
        return round(len(self.__n_gramms & check_str_n_gramms) / len(self.__n_gramms | check_str_n_gramms) * 100)

    @staticmethod
    def split_into_n_gramms(token_str, length_n_gramm):
        if length_n_gramm <= 0:
            return set()
        n_gramms = []
        for i in range(len(token_str) - length_n_gramm + 1):
            n_gramms.append(token_str[i:i + length_n_gramm])
        return set(n_gramms)
