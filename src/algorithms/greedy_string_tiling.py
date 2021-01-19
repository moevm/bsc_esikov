from src.algorithms.plagiarism_src_detector import PlagiarismSrcDetector


class GreedyStringTiling(PlagiarismSrcDetector):
    def __init__(self, token_str):
        self.__token_str = token_str
        self.__min_match_len = 2

    def search(self, search_tokens_str):
        tiles = []
        matches = []
        max_match = self.__min_match_len + 1
        source_marked = {}
        search_marked = {}
        while max_match > self.__min_match_len:
            max_match = self.__min_match_len
            for p in range(len(self.__token_str)):
                for t in range(len(search_tokens_str)):
                    j = 0
                    while p + j < len(self.__token_str) and t + j < len(search_tokens_str) and self.__token_str[p + j]\
                            == search_tokens_str[t + j] and p + j not in source_marked and t + j not in search_marked:
                        j += 1
                    if j == max_match:
                        matches.append({"p": p, "t": t, "j": j})
                    if j > max_match:
                        matches = [{"p": p, "t": t, "j": j}]
                        max_match = j
            for match in matches:
                if not self.is_marked_match(source_marked, match["p"], match["j"]) and not self.is_marked_match(search_marked, match["t"], match["j"]):
                    for k in range(match["j"]):
                        source_marked[match["p"] + k] = True
                        search_marked[match["t"] + k] = True
                    tiles.append(self.__token_str[match["p"]:match["p"] + match["j"]])
        return tiles

    @staticmethod
    def is_marked_match(marked_string_dict, begin, length):
        if begin in marked_string_dict or begin + length - 1 in marked_string_dict:
            return True
        else:
            return False
