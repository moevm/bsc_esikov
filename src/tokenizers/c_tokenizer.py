import re
from src.tokenizers.tokenizer import Tokenizer


class CTokenizer(Tokenizer):
    INT_TYPES = "|".join(["unsigned long long int", "unsigned long long", "unsigned long int", "unsigned long",
                     "unsigned int", "unsigned short int", "unsigned short", "unsigned", "signed long long int",
                     "signed long long", "signed long int", "signed long", "signed short int", "signed short",
                     "signed int", "signed", "long long int", "long long", "long int", "long", "short int",
                     "short", "int"]).replace(" ", "")
    CHAR_TYPES = "|".join(["signed char", "unsigned char", "char"]).replace(" ", "")
    FLOAT_TYPES = "|".join(["long double", "double", "float"]).replace(" ", "")
    BORDER = "$"
    NOT_TOKEN = "X"         # Используется при токенизации, не является конечным токеном
    TOKENS = {
        "int": "N",         # - Number - целое число
        "double": "D",      # - Double - дробное число
        "char": "B",        # - Byte - однобайтовый тип (char)
        "ptr": "P",         # - Pointer - указатель
        "call": "C",        # - Call - вызов функции
        "assign": "A",      # - Assign - присваивание
        "func": "F",        # - Function - определение функции
        "cast": "T",        # - Type - приведение типов
        "math": "M",        # - Math - математические операторы + инкремент и декремент
        "return": "R",      # - Return - возврат значения из функции
        "if": "I",          # - If - условные конструкции
        "cycle": "S",       # - Series - циклы
        "compare": "E",     # - сравнения
        "logic": "L",       # - Logic - логические операции
        "shift": "U",       # - Upheaval - побитовые операции сдвига
        "control": "G",     # - Governance - управляющие конструкции
        "struct": "V",      # - Var - структуры
    }

    @staticmethod
    def token_str():
        token_str = ""
        for token in CTokenizer.TOKENS.values():
            token_str += token
        return token_str

    @staticmethod
    def border_token(token_key):
        return CTokenizer.BORDER + CTokenizer.TOKENS[token_key] + CTokenizer.BORDER

    def _process(self, src):
        # Исправление названия переменной, содержащей в себе имя типа данных языка C
        main_types = "short|int|long|signed|unsigned|char|float|double"
        change_code = re.sub(r'(\w({types}))|(({types})\w)'.format(types=main_types), CTokenizer.NOT_TOKEN, src)
        change_code = self.clear_space(change_code)
        # Замена названий переменных, которые совпадают с именами токенов
        change_code = re.sub(r'[{tokens}]'.format(tokens=CTokenizer.token_str()), CTokenizer.NOT_TOKEN, change_code)
        # Токенизация возврата из функции
        change_code = re.sub(r'return', CTokenizer.border_token("return"), change_code)
        # Токенизация указателей на функцию
        change_code = re.sub(r'\w+\*?\(\*[\w\[\]]+\)\(([\w$.*\[\]]*,*)*\)', CTokenizer.border_token("ptr"), change_code)
        # Удаление break из switch
        change_code = CTokenizer.replace_break_in_switch(change_code)
        # Удаление ключевого слова switch, чтобы оно не было токенизировано как определение функции
        change_code = re.sub(r'switch[^{]*{', "", change_code)
        # Токенизация определения функции
        change_code = re.sub(r'([a-zA-Z_][\w*]*)\(([\w$.*\[\]]*,*)*\){', CTokenizer.border_token("func") + "{", change_code)
        # Токенизация функции, возвращающей указатель на функцию
        change_code = re.sub(r'\w+\*?\(\*[\w\[\]]+\(([\w$.*\[\]]*,*)*\)\)\(([\w$.*\[\]]*,*)*\){', CTokenizer.border_token("func") + "{", change_code)
        # Токенизация вызова функции
        change_code = re.sub(r'([a-zA-Z_]\w*)\([^;!><|&]*\);', CTokenizer.border_token("call") + ";", change_code)
        # Токенизация приведения типа
        change_code = re.sub(r'\([a-zA-Z_]\w*\**\)', CTokenizer.border_token("cast"), change_code)
        # Токенизация указателя на структуру
        change_code = re.sub(r'struct([a-zA-Z_]\w*;?)?\*', CTokenizer.border_token("ptr"), change_code)
        # Токенизация структур
        change_code = re.sub(r'(struct|union)([a-zA-Z_]\w*;?)?', CTokenizer.border_token("struct"), change_code)
        # Токенизация основных типов данных
        change_code = re.sub(r'({int_types}|{char_types}|{float_types}|void)\*+([a-zA-Z_]\w*;?)?'.format(
            int_types=CTokenizer.INT_TYPES, char_types=CTokenizer.CHAR_TYPES, float_types=CTokenizer.FLOAT_TYPES), CTokenizer.border_token("ptr"), change_code)
        change_code = re.sub(r'({char_types})([a-zA-Z_]\w*;?)?'.format(char_types=CTokenizer.CHAR_TYPES), CTokenizer.border_token("char"), change_code)
        change_code = re.sub(r'({float_types})([a-zA-Z_]\w*;?)?'.format(float_types=CTokenizer.FLOAT_TYPES), CTokenizer.border_token("double"), change_code)
        change_code = re.sub(r'({int_types})([a-zA-Z_]\w*;?)?'.format(int_types=CTokenizer.INT_TYPES), CTokenizer.border_token("int"), change_code)
        # Токенизация свитч
        change_code = re.sub(r'(case|default)[^:]*:{?', CTokenizer.border_token("if") + "{", change_code)
        # Токенизация условных конструкций
        change_code = re.sub(r'(((if|elseif)\([^)]*\))|else)', CTokenizer.border_token("if"), change_code)
        # Токенизация циклов
        change_code = re.sub(r'do', CTokenizer.border_token("cycle"), change_code)
        change_code = re.sub(r'while\([^;]*\);', "", change_code)
        change_code = re.sub(r'(for|while)\([^{}]*\){', CTokenizer.border_token("cycle") + "{", change_code)
        change_code = re.sub(r'(for|while)\([^{}]*\)[\w$]', CTokenizer.border_token("cycle") + CTokenizer.NOT_TOKEN, change_code)
        # Токенизация управляющих конструкций
        change_code = re.sub(r'continue|break|goto', CTokenizer.border_token("control"), change_code)
        # Токенизация сочетаний оператора присваивания
        change_code = re.sub(r'[+\-*/%]=', CTokenizer.border_token("assign") + CTokenizer.border_token("math"), change_code)
        change_code = re.sub(r'(<<|>>|&|\^|\|)=', CTokenizer.border_token("assign") + CTokenizer.border_token("shift"), change_code)
        # Токенизация математических выражений
        change_code = re.sub(r'(([a-zA-Z_]\w*)\+\+)|(\+\+[a-zA-Z_]\w*)', CTokenizer.border_token("math"), change_code)
        change_code = re.sub(r'(([a-zA-Z_]\w*)--)|(--[a-zA-Z_]\w*)', CTokenizer.border_token("math"), change_code)
        change_code = re.sub(r'[^={},(]\*', CTokenizer.border_token("math"), change_code)
        change_code = re.sub(r'[^={}><|&][+\-/%][^>]', CTokenizer.border_token("math"), change_code)
        # Токенизация логических операций
        change_code = re.sub(r'&&|\|\||!', CTokenizer.border_token("logic"), change_code)
        # Токенизация побитовых операций
        change_code = re.sub(r'[^={}><|&](<<|>>|&|\^|\|)', CTokenizer.border_token("shift"), change_code)
        change_code = re.sub(r'~', CTokenizer.border_token("shift"), change_code)
        # Токенизация сравнений
        change_code = re.sub(r'==|([^-]>)|<|<=|>=|!=', CTokenizer.border_token("compare"), change_code)
        # Токенизация присваивания
        change_code = re.sub(r'=({[^;]*};)?', CTokenizer.border_token("assign"), change_code)
        # Удаление всех символов не соответствующих токенам и принудительная расстановка фигурных скобок
        needed_symbols = r'[^{};' + r'{tokens}'.format(tokens=CTokenizer.token_str()) + r']*'
        change_code = re.sub(needed_symbols, "", change_code)
        change_code = CTokenizer.place_curly_braces_in_src(change_code)
        change_code = re.sub(r';*', "", change_code)
        print(change_code, "\n")

        return change_code

    @staticmethod
    def place_curly_braces_in_src(tokens):
        i = count_brace = 0
        change_tokens = tokens
        while True:
            if i >= len(change_tokens):
                return change_tokens
            if change_tokens[i] == CTokenizer.TOKENS["if"] or change_tokens[i] == CTokenizer.TOKENS["cycle"]:
                i += 1
                if i < len(change_tokens) and change_tokens[i] != "{":
                    count_brace += 1
                    change_tokens = change_tokens[:i] + "{" + change_tokens[i:]
            if change_tokens[i] == ";" and count_brace != 0:
                while count_brace != 0:
                    i += 1
                    change_tokens = change_tokens[:i] + "}" + change_tokens[i:]
                    count_brace -= 1
            i += 1

    @staticmethod
    def replace_break_in_switch(src_without_space, begin_find=0, is_replace_last_symbol_switch=True):
        index = src_without_space.find("switch(", begin_find)
        if index != -1:
            end_switch = CTokenizer.find_index_end_switch(src_without_space, index)
            change_src = src_without_space
            if end_switch is not None:
                temp_str = src_without_space[index:end_switch+1]
                temp_str = re.sub(r'break;}?', CTokenizer.NOT_TOKEN * 5 + ";}", temp_str)
                change_src = src_without_space[:index] + temp_str + src_without_space[end_switch+1:]
                if is_replace_last_symbol_switch is True:
                    change_src = change_src[:end_switch] + ";" + change_src[end_switch+1:]
            return CTokenizer.replace_break_in_switch(change_src, end_switch)
        return src_without_space

    @staticmethod
    def find_index_end_switch(src_without_space, index=0):
        for i in range(index, len(src_without_space)):
            if src_without_space[i] == "}":
                if i + 1 < len(src_without_space):
                    if src_without_space[i + 1] == "}":
                        return i + 1
                    else:
                        if src_without_space.find("case", i + 1, i + 5) != -1:
                            return CTokenizer.find_index_end_switch(src_without_space, i + 2)
                        else:
                            return i
                else:
                    return i
        return None

    @staticmethod
    def clear_import(src):
        result = re.sub(r'\s*#include\s*[<"].*[>"]\s*', "", src)
        return result

    @staticmethod
    def clear_comments(src):
        result = re.sub(r'//\s*.*(\n|$)', "", src)
        result = re.sub(r'//*(.|\n)*/*/', "", result)
        return result
