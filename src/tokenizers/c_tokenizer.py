import re
from operator import attrgetter
from src.tokenizers.tokenizer import Tokenizer
from src.token import Token


class CTokenizer(Tokenizer):
    INT_TYPES = "|".join(["unsigned long long int", "unsigned long long", "unsigned long int", "unsigned long",
                          "unsigned int", "unsigned short int", "unsigned short", "unsigned", "signed long long int",
                          "signed long long", "signed long int", "signed long", "signed short int", "signed short",
                          "signed int", "signed", "long long int", "long long", "long int", "long", "short int",
                          "short", "int"])
    CHAR_TYPES = "|".join(["signed char", "unsigned char", "char"])
    FLOAT_TYPES = "|".join(["long double", "double", "float"])
    BORDER = "$"
    NOT_TOKEN = "X"  # Используется при токенизации, не является конечным токеном
    TOKENS = {
        "int": "N",  # - Number - целое число
        "double": "D",  # - Double - дробное число
        "char": "B",  # - Byte - однобайтовый тип (char)
        "ptr": "P",  # - Pointer - указатель
        "call": "C",  # - Call - вызов функции
        "assign": "A",  # - Assign - присваивание
        "func": "F",  # - Function - определение функции
        "cast": "T",  # - Type - приведение типов
        "math": "M",  # - Math - математические операторы + инкремент и декремент
        "return": "R",  # - Return - возврат значения из функции
        "if": "I",  # - If - условные конструкции
        "cycle": "S",  # - Series - циклы
        "compare": "E",  # - сравнения
        "logic": "L",  # - Logic - логические операции
        "shift": "U",  # - Upheaval - побитовые операции сдвига
        "control": "G",  # - Governance - управляющие конструкции
        "struct": "V",  # - Var - структуры
    }

    @staticmethod
    def clear_import(src):
        result = re.sub(r'\s*#include\s*[<"][^<>"]+[>"]\s*', "", src)
        return result

    @staticmethod
    def clear_comments(src):
        result = re.sub(r'//[^\n]*(\n|$)', "", src)
        result = re.sub(r'/\*.*?\*/', "", result, flags=re.DOTALL)
        return result

    @staticmethod
    def token_str():
        token_str = ""
        for token in CTokenizer.TOKENS.values():
            token_str += token
        return token_str

    @staticmethod
    def border_token(token_key):
        return CTokenizer.BORDER + CTokenizer.TOKENS[token_key] + CTokenizer.BORDER

    def _fast_process(self, src):
        # Исправление названия переменной, содержащей в себе имя типа данных языка C
        main_types = "short|int|long|signed|unsigned|char|float|double"
        change_code = re.sub(r'(\w({types}))|(({types})\w)'.format(types=main_types), CTokenizer.NOT_TOKEN, src)
        change_code = self.clear_space(change_code)
        # Замена названий переменных, которые совпадают с именами токенов
        change_code = re.sub(r'[{tokens}]'.format(tokens=CTokenizer.token_str()), CTokenizer.NOT_TOKEN, change_code)
        # Токенизация возврата из функции
        change_code = re.sub(r'return', CTokenizer.border_token("return"), change_code)
        # Токенизация функции, возвращающей указатель на функцию
        change_code = re.sub(r'\w+\**\(\*+[\w\[\]]+\(([\w$.*\[\]]*,*)*\)\)\(([\w$.*\[\]]*,*)*\){', CTokenizer.border_token("func") + "{", change_code)
        # Токенизация указателей на функцию
        change_code = re.sub(r'\w+\**\(\*+[\w\[\]]+\)\(([\w$.*\[\]]*,*)*\)', CTokenizer.border_token("ptr"), change_code)
        # Удаление break из switch
        change_code = CTokenizer.replace_break_in_switch(change_code)
        # Удаление ключевого слова switch, чтобы оно не было токенизировано как определение функции
        change_code = re.sub(r'switch[^{]*{', "", change_code)
        # Токенизация условных конструкций
        change_code = re.sub(r'(((if|elseif)\([^)]*\))|else)', CTokenizer.border_token("if"), change_code)
        # Токенизация определения функции
        change_code = re.sub(r'[\w*]+\([^{]*\){', CTokenizer.border_token("func") + "{", change_code)
        # Токенизация вызова функции
        change_code = re.sub(r'([a-zA-Z_]\w*)\([^;!><|&]*\);', CTokenizer.border_token("call") + ";", change_code)
        # Токенизация приведения типа
        change_code = re.sub(r'\([a-zA-Z_]\w*\**\)', CTokenizer.border_token("cast"), change_code)
        # Токенизация указателя на структуру
        change_code = re.sub(r'struct([a-zA-Z_]\w*;?)?\*', CTokenizer.border_token("ptr"), change_code)
        # Токенизация структур
        change_code = re.sub(r'(struct|union)([a-zA-Z_]\w*;?)?', CTokenizer.border_token("struct"), change_code)
        # Токенизация основных типов данных
        change_code = re.sub(r'({int_types}|{char_types}|{float_types}|void)\*+([a-zA-Z_]\w*)?'\
                             .format(
                                        int_types=CTokenizer.INT_TYPES.replace(" ", ""),
                                        char_types=CTokenizer.CHAR_TYPES.replace(" ", ""),
                                        float_types=CTokenizer.FLOAT_TYPES.replace(" ", "")
                             ), CTokenizer.border_token("ptr"), change_code)
        change_code = re.sub(r'({char_types})([a-zA-Z_]\w*)?'.format(char_types=CTokenizer.CHAR_TYPES.replace(" ", "")),
                             CTokenizer.border_token("char"), change_code)
        change_code = re.sub( r'({float_types})([a-zA-Z_]\w*)?'.format(float_types=CTokenizer.FLOAT_TYPES.replace(" ", "")),
                              CTokenizer.border_token("double"), change_code)
        change_code = re.sub(r'({int_types})([a-zA-Z_]\w*)?'.format(int_types=CTokenizer.INT_TYPES.replace(" ", "")),
                             CTokenizer.border_token("int"), change_code)
        # Токенизация свитч
        change_code = re.sub(r'(case|default)[^:]*:{?', CTokenizer.border_token("if") + "{", change_code)
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
        change_code = re.sub(r';', "", change_code)
        # print(change_code, "\n")

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
        match = re.search(r'\bswitch\s*\(', src_without_space[begin_find:], flags=re.ASCII)
        if match is not None:
            end_switch = CTokenizer.find_index_end_switch(src_without_space, match.end())
            change_src = src_without_space
            if end_switch is not None:
                temp_str = src_without_space[match.end():end_switch + 1]
                for match_break in re.finditer(r'\bbreak;\s*}?', temp_str, flags=re.ASCII):
                    temp_str = temp_str[:match_break.start()] + CTokenizer.NOT_TOKEN * (match_break.end() - match_break.start() - 1) + "}" + temp_str[match_break.end():]
                change_src = src_without_space[:match.end()] + temp_str + src_without_space[end_switch + 1:]
                if is_replace_last_symbol_switch is True:
                    change_src = change_src[:end_switch] + ";" + change_src[end_switch + 1:]
            return CTokenizer.replace_break_in_switch(change_src, end_switch)
        return src_without_space

    @staticmethod
    def find_index_end_switch(src, index=0):
        for i in range(index, len(src)):
            if src[i] == "}":
                if i + 1 < len(src):
                    while src[i + 1] == " " or src[i + 1] == "\n" or src[i + 1] == "\t":
                        i += 1
                    if src[i + 1] == "}":
                        return i + 1
                    else:
                        if src.find("case", i + 1, i + 5) != -1:
                            return CTokenizer.find_index_end_switch(src, i + 2)
                        else:
                            return i
                else:
                    return i
        return None

    @staticmethod
    def replace_comments(src):
        comment_tokens = CTokenizer.search_tokens(src, r'//[^\n]*(\n|$)', "control", re.ASCII + re.MULTILINE)
        src = CTokenizer.replace_tokens_in_src(src, comment_tokens, " ", True)
        comment_tokens = CTokenizer.search_tokens(src, r'/\*.*?\*/', "control", re.ASCII + re.DOTALL)
        src = CTokenizer.replace_tokens_in_src(src, comment_tokens, " ", True)
        return src

    @staticmethod
    def replace_import(src):
        import_tokens = CTokenizer.search_tokens(src, r'#include\s*[<"][^<>"]+[>"]', "control", re.ASCII)
        src = CTokenizer.replace_tokens_in_src(src, import_tokens, " ", True)
        return src

    def _process(self, src):
        tokens = []
        # Токенизация возврата из функции
        tokens += CTokenizer.search_tokens(src, r'\breturn\b[^;]*;', "return")

        # Токенизация указателей на функцию
        regex_for_func_ptr = r'\w+(\s*\*\s*)*\s*\((\s*\*\s*)+[\w+\[\]]+\s*\)\s*\([^=;]*\)\s*(?=[;=])'
        function_pointer_tokens = CTokenizer.search_tokens(src, regex_for_func_ptr, "ptr")
        src = CTokenizer.replace_tokens_in_src(src, function_pointer_tokens)
        tokens += function_pointer_tokens

        # Токенизация определения функции, возвращающей указатель на функцию
        regex_for_func_def = r'\w+(\s*\*\s*)*\s*\((\s*\*?\s*)*\w+\s*\([^{]*\)\s*\)\s*\([^{]*\)\s*(?={)'
        function_tokens = CTokenizer.search_tokens(src, regex_for_func_def, "func")
        src = CTokenizer.replace_tokens_in_src(src, function_tokens)
        tokens += function_tokens

        # Получение токенов не расставленных фигурных скобок после for, while, do, if, else
        tokens += CTokenizer.get_tokens_missing_curly_braces(src)

        # Токенизация циклов
        tokens += CTokenizer.search_tokens(src, r'\bdo\b', "cycle")
        while_from_do_tokens = CTokenizer.search_tokens(src, r'while\s*\([^;]*\)\s*;', "cycle")
        src = CTokenizer.replace_tokens_in_src(src, while_from_do_tokens)
        cycle_tokens = CTokenizer.search_tokens(src, r'\b(for|while)\b\s*\([^{]+?\)\s*(?=[{\w])', "cycle")
        src = CTokenizer.replace_tokens_in_src(src, cycle_tokens)
        tokens += cycle_tokens

        # Удаление закрывающей } в switch
        #   Специальный символ $ используется в дальнейшем при токенизации как окончание switch
        src = CTokenizer.replace_close_brace_in_switch(src, "$")

        # Удаление break из switch
        for match in re.finditer(r'(\bcase|\bdefault)[^:]*:.*?(\bbreak\s*;\s*}?)', src, flags=re.ASCII + re.DOTALL):
            src = src[:match.start(2)] + CTokenizer.NOT_TOKEN * (match.end(2) - match.start(2) - 1) + src[match.end(2) - 1:]

        # Удаление ключевого слова switch, чтобы оно не было токенизировано как определение функции
        for match in re.finditer(r'\bswitch[^{]*{', src, flags=re.ASCII):
            src = src[:match.start()] + ';' * (match.end() - match.start()) + src[match.end():]

        # Токенизация switch
        for match in re.finditer(r'(\b((case|default)\b[^:]*?:)\s*[{\w])([^}$]*?(?=(}|\$|\bcase\b|\bdefault\b)))', src, flags=re.ASCII):  # $ используется
            token = Token(CTokenizer.TOKENS["if"], match.start(1), match.end(1))
            if src[token.end - 1] != "{":
                tokens.append(Token("{", token.end - 2, token.end - 2))
            tokens.append(token)
            src = src[:match.start(2)] + ';' * (match.end(2) - match.start(2)) + src[match.end(2):]
            if src[match.start(5)] != "}":
                tokens.append(Token("}", match.start(5) - 1, match.start(5) - 1))

        # Токенизация условных конструкций
        if_else_tokens = CTokenizer.search_tokens(src, r'\b(if|else\s*if)\s*\([^{;]+?\)\s*(?=[{\w])|\belse\b', "if")
        src = CTokenizer.replace_tokens_in_src(src, if_else_tokens)
        tokens += if_else_tokens
        # Токенизация определения функции
        function_tokens = CTokenizer.search_tokens(src, r'\w+((\s*\*\s*)+|\s+)\w+\s*\([^{]*\)\s*(?={)', "func")
        src = CTokenizer.replace_tokens_in_src(src, function_tokens)
        tokens += function_tokens

        # Токенизация вызова функции
        call_tokens = CTokenizer.search_tokens(src, r'\w+\s*\([^;{]*?\)\s*;', "call")
        src = CTokenizer.replace_tokens_in_src(src, call_tokens, is_full_replace=False)
        tokens += call_tokens

        # Токенизация приведения типа
        type_cast_tokens = CTokenizer.search_tokens(src, r'\(\s*\w+(\s*\*?\s*)*\)', "cast")
        src = CTokenizer.replace_tokens_in_src(src, type_cast_tokens)
        tokens += type_cast_tokens

        # Токенизация указателя на структуру
        struct_pointers_tokens = CTokenizer.search_tokens(src, r'(struct|union)\s*\w+(\s*\*+\s*)+\w+', "ptr")
        src = CTokenizer.replace_tokens_in_src(src, struct_pointers_tokens)
        tokens += struct_pointers_tokens

        # Токенизация структур
        tokens += CTokenizer.search_tokens(src, r'(struct|union)(\s+\w+)?\s*(?={)', "struct")
        regex_for_struct_var = r'(struct|union)\s+\w+\s+\w+[\[\]\d]*(\s*,\s*\w+[\[\]\d]*\s*)*\s*(?=[;=])'
        tokens += CTokenizer.search_tokens(src, regex_for_struct_var, "struct")

        # Токенизация основных типов данных
        regex_for_ptr = r'({int_types}|{char_types}|{float_types}|void)(\s*\*+\s*)+(\s*const\s+)?\w+[\[\]\d:]*(\s*,\s*\w+[\[\]\d]*\s*)*\s*(?=[;=])'\
                        .format(
                            int_types=CTokenizer.INT_TYPES,
                            char_types=CTokenizer.CHAR_TYPES,
                            float_types=CTokenizer.FLOAT_TYPES
                        )
        pointers = CTokenizer.search_tokens(src, regex_for_ptr, "ptr")
        src = CTokenizer.replace_tokens_in_src(src, pointers)
        tokens += pointers
        regex_for_char = r'({char_types})\s+\w+[\[\]\d:]*(\s*,\s*\w+[\[\]\d]*\s*)*\s*(?=[;=])'\
                         .format(char_types=CTokenizer.CHAR_TYPES)
        tokens += CTokenizer.search_tokens(src, regex_for_char, "char")
        regex_for_float = r'({float_types})\s+\w+[\[\]\d:]*(\s*,\s*\w+[\[\]\d]*\s*)*\s*(?=[;=])'\
                          .format(float_types=CTokenizer.FLOAT_TYPES)
        tokens += CTokenizer.search_tokens(src, regex_for_float, "double")
        regex_for_int = r'({int_types})\s+\w+[\[\]\d:]*(\s*,\s*\w+[\[\]\d]*\s*)*\s*(?=[;=])'\
                        .format(int_types=CTokenizer.INT_TYPES)
        tokens += CTokenizer.search_tokens(src, regex_for_int, "int")

        # Токенизация управляющих конструкций
        tokens += CTokenizer.search_tokens(src, r'\bcontinue\s*;|\bbreak\s*;|\bgoto\s+\w+;', "control")

        # Токенизация сочетаний оператора присваивания
        #   Специальный символ @ используется для токенизации этих сочетаний в правильном порядке
        src = re.sub(r'(<<|>>|&|\^|\||\+|-|\*|/|%)=', r'@\1', src)

        # Токенизация математических выражений
        tokens += CTokenizer.search_tokens(src, r'\w+\+\+|\+\+\w+', "math")
        tokens += CTokenizer.search_tokens(src, r'\w+--|--\w+', "math")
        tokens += CTokenizer.search_tokens(src, r'[^@={},(\s]\s*\*', "math")  # @ используется
        tokens += CTokenizer.search_tokens(src, r'(?<=@)\*', "math")  # @ используется
        tokens += CTokenizer.search_tokens(src, r'[^@={}><|&\s+-]\s*[+\-/%]\s*[^>\s+-]', "math")  # @ используется
        tokens += CTokenizer.search_tokens(src, r'(?<=@)[+\-/%]\s*[^>\s+-]', "math")  # @ используется

        # Токенизация логических операций
        tokens += CTokenizer.search_tokens(src, r'&&|\|\||!', "logic")

        # Токенизация побитовых операций
        tokens += CTokenizer.search_tokens(src, r'\w+\s*(<<|>>|&|\^|\|)\s*\w+', "shift")
        tokens += CTokenizer.search_tokens(src, r'(?<=@)(<<|>>|&|\^|\|)\s*\w+', "shift")  # @ используется
        tokens += CTokenizer.search_tokens(src, r'~', "shift")

        # Токенизация сравнений
        tokens += CTokenizer.search_tokens(src, r'==|((?<!-)>)|(?<!<)<[^<]|<=|>=|!=', "compare")

        # Токенизация присваивания
        assign_tokens = CTokenizer.search_tokens(src, r'[=@]\s*{[^;]*}\s*;', "assign")  # @ используется
        src = CTokenizer.replace_tokens_in_src(src, assign_tokens)
        tokens += assign_tokens
        tokens += CTokenizer.search_tokens(src, r'(?<!=)[=@][^=;]+;?', "assign")  # @ используется

        # Токенизация фигурных скобок
        for match in re.finditer(r'{', src, flags=re.ASCII):
            tokens.append(Token("{", match.start(), match.end()))
        for match in re.finditer(r'}', src, flags=re.ASCII):
            tokens.append(Token("}", match.start(), match.end()))

        return sorted(tokens, key=attrgetter('start', 'end'))

    @staticmethod
    def search_tokens(src, pattern, token_key, flags=re.ASCII):
        tokens = []
        for match in re.finditer(pattern, src, flags=flags):
            tokens.append(Token(CTokenizer.TOKENS[token_key], match.start(), match.end()))
        return tokens

    @staticmethod
    def replace_tokens_in_src(src, tokens, replace=".", is_full_replace=True):
        for token in tokens:
            if is_full_replace is True:
                src = src[:token.start] + replace * (token.end - token.start) + src[token.end:]
            else:
                src = src[:token.start] + replace * (token.end - token.start - 1) + src[token.end - 1:]
        return src

    @staticmethod
    def get_function_names(src):
        functions = set()
        for match in re.finditer(r'\w+(\s*\*\s*)*\s*\((\s*\*?\s*)*(\w+)\s*\([^{]*\)\s*\)\s*\([^{]*\)\s*{', src, flags=re.ASCII):
            functions |= {match[3]}
        for match in re.finditer(r'\w+((\s*\*\s*)+|\s+)(\w+)\s*\([^{]*\)\s*{', src, flags=re.ASCII):
            functions |= {match[3]}
        return list(functions)

    @staticmethod
    def get_tokens_missing_curly_braces(src):
        tokens = []

        for match in re.finditer(r'\belse\s*([^;{]+;)\s*', src, flags=re.ASCII):
            tokens.append(Token("{", match.start(1) - 1, match.start(1) - 1))
            tokens.append(Token("}", match.end(1) - 1, match.end(1) - 1))

        for match in re.finditer(r'\bdo[^\w]([^;]+;)', src, flags=re.ASCII):
            tokens.append(Token("{", match.start(1) - 1, match.start(1) - 1))
            tokens.append(Token("}", match.end(1) - 1, match.end(1) - 1))

        for match in re.finditer(r'\bfor\s*\((([^;]*;\s*){2}[^)]*)\)', src, flags=re.ASCII):
            src = src[:match.start(1)] + "." * (match.end(1) - match.start(1)) + src[match.end(1):]

        keywords = ["while", "if", "for"]
        for word in keywords:
            for match in re.finditer(r'(?=(\b' + word + r'\s*\([^;{]+?\)\s*([^;{]+;)\s*))', src, flags=re.ASCII):
                tokens.append(Token("{", match.start(2) - 1, match.start(2) - 1))
                i = match.end(1)
                if i + 4 < len(src) and word != "if":
                    if src[i] == 'e' and src[i + 1] == 'l' and src[i + 2] == 's' and src[i + 3] == 'e' \
                            and not str.isalpha(src[i + 4]):
                        while i < len(src) and src[i] != ';':
                            i += 1
                        tokens.append(Token("}", i, i))
                        continue
                tokens.append(Token("}", match.end(2) - 1, match.end(2) - 1))

        return tokens

    @staticmethod
    def replace_close_brace_in_switch(src, symbol):
        for match in re.finditer(r'\bswitch\b[^{]+{', src, flags=re.ASCII):
            i = match.end()
            count_close_brace = 1
            while i < len(src):
                if src[i] == '{':
                    count_close_brace += 1
                if src[i] == '}':
                    count_close_brace -= 1
                    if count_close_brace == 0:
                        src = src[:i] + symbol + src[i + 1:]
                        break
                i += 1
        return src
