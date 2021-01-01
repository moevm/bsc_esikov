import re
from src.tokenizers.tokenizer import Tokenizer


class CTokenizer(Tokenizer):
    @property
    def keywords(self):
        return "c keywords"

    def _process(self, src):
        print("tokenize c-file\n")
        src = re.sub(r'(int|long) [a-zA-Z_]\w*', "INT_NUMBER_", src)
        src = re.sub(r'(char|signed char) [a-zA-Z_]\w*', "CHAR_", src)
        src = re.sub(r'(char|int)\*+', "POINTER_", src)
        src = re.sub(r'\(([a-zA-Z_]\w*)\)', "TYPE_CAST_", src)
        src = re.sub(r'(for|while)', "CYCLE_", src)
        #src111 = re.sub(r'([a-zA-Z_]\w*)\(.*\)', "FUNCTION_", src111)
        src = re.sub(r'([a-zA-Z_]\w*)\(.*\)', "№", src)

        src = re.sub(r'return \w*;', "RETURN_", src)
        src = re.sub(r'(([a-zA-Z_]\w*)\+\+)|(\+\+[a-zA-Z_]\w*)', "INC_", src)
        src = re.sub(r'(([a-zA-Z_]\w*)--)|(--[a-zA-Z_]\w*)', "DEC_", src)
        #src111 = re.sub(r'=\s*[^F]?[^U]?[^N]?[^C]?[^T]?[^I]?[^O]?[^N]?[^_]?[^;]*;', "ASSIGN_", src111)
        src = re.sub(r'=\s*[^№]\w*;', "ASSIGN_", src)
        src = re.sub(r"=\s*[^№][\w'\\]*;", "ASSIGN_", src)
        src = re.sub(r'=\s*№', "ASSIGN_FUNCTION_", src)
        src = re.sub(r'№', "FUNCTION_", src)

        return src

    def _clear_import(self, src):
        result = re.sub(r'#include\s*[<"]\S*[>"]\s*', "", src)
        return result

    def _clear_special_characters(self, src):
        return src

    def _clear_comments(self, src):
        result = re.sub(r'//\s*.*(\n|$)', "", src)
        result = re.sub(r'//*(.|\n)*/*/', "", result)
        return result
