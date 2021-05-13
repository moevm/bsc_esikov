from src.models.token import Token


class Similarity:
    def __init__(self, check_file, detected_file, similarity_tokens_sequences):
        self.__check_file = check_file
        self.__detected_file = detected_file
        self.__similarity_tokens_sequences = similarity_tokens_sequences

    def get_similarity_src(self):
        check_file_similarity_src = []
        detected_file_similarity_src = []
        for sim_tokens_str in self.__similarity_tokens_sequences:
            check_file_similarity_src.append(self._get_str_src_from_token_str(self.__check_file, sim_tokens_str))
            detected_file_similarity_src.append(self._get_str_src_from_token_str(self.__detected_file, sim_tokens_str))
        return check_file_similarity_src, detected_file_similarity_src

    def _get_str_src_from_token_str(self, src_file, sim_tokens_str):
        start, end = Token.find_border_tokens_str_in_token_list(src_file.tokens, sim_tokens_str)
        return src_file.src[start:end]

    def get_list_zip_similarity_fragments(self):
        check_file_similarity_src, detected_file_similarity_src = self.get_similarity_src()
        return list(zip(check_file_similarity_src, detected_file_similarity_src))

    @property
    def check_file_path(self):
        return self.__check_file.path

    @property
    def detected_file_path(self):
        return self.__detected_file.path

    @property
    def check_file_source(self):
        return self.__check_file.source

    @property
    def detected_file_source(self):
        return self.__detected_file.source

    @property
    def similarity_percentage(self):
        return self.__detected_file.similarity_percentage
