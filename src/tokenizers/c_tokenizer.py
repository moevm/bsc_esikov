import re
from src.tokenizers.tokenizer import Tokenizer


class CTokenizer(Tokenizer):
    __int_types = "unsignedlonglongint|unsignedlonglong|unsignedlongint|unsignedlong|unsignedint|unsignedshortint|" \
                  "unsignedshort|unsigned|signedlonglongint|signedlonglong|signedlongint|signedlong|signedshortint|" \
                  "signedshort|signedint|signed|longlongint|longlong|longint|long|shortint|short|int"
    __char_types = "char|signedchar|unsignedchar"
    __float_types = "float|double|longdouble"

    @property
    def keywords(self):
        return "c keywords"

    # tokens C:
    # N - Number - целое число
    # D - Double - дробное число
    # B - Byte - однобайтовый тип (char)
    # P - Pointer - указатель
    # C - Call - вызов функции
    # A - Assign - присваивание
    # F - Function - функция
    # T - Type - приведение типов
    # M - Math - математические операторы + инкремент и декремент
    # R - Return - возврат значения из функции
    # I - If - условные конструкции
    # S - Series - циклы
    # E - сравнения
    # L - Logic - логические операции
    # U - Upheaval - побитовые операции сдвига
    # G - Governance - управляющие конструкции
    # V - Var - структуры
    def _process(self, src):
        # Исправление названия переменной, содержащей в себе имя типа данных языка C
        main_types = "short|int|long|signed|unsigned|char|float|double"
        change_code = re.sub(r'(\w({types}))|(({types})\w)'.format(types=main_types), "z", src)
        change_code = self.clear_space(change_code)
        print(change_code, "\n")
        # Замена названий переменных, которые совпадают с именами токенов
        change_code = re.sub(r'[NDBPCAFTMRISELUGV]', "X", change_code)
        # Токенизация возврата из функции
        change_code = re.sub(r'return', "$R$", change_code)
        # Токенизация указателей на функцию
        change_code = re.sub(r'\w+\*?\(\*[\w\[\]]+\)\(([\w$.*\[\]]*,*)*\)', "$P$", change_code)
        # Токенизация определения функции
        change_code = re.sub(r'([a-zA-Z_][\w*]*)\(([\w$.*\[\]]*,*)*\){', "$F${", change_code)
        # Токенизация функции, возвращающей указатель на функцию
        change_code = re.sub(r'\w+\*?\(\*[\w\[\]]+\(([\w$.*\[\]]*,*)*\)\)\(([\w$.*\[\]]*,*)*\){', "$F${", change_code)
        # Токенизация вызова функции
        change_code = re.sub(r'([a-zA-Z_]\w*)\([^;!><|&]*\)(;|!=|,|==|>|<|>=|<=|&&|\|\|)', "$C$", change_code)
        # Токенизация приведения типа
        change_code = re.sub(r'\([a-zA-Z_]\w*\**\)', "$T$", change_code)
        # Токенизация указателя на структуру
        change_code = re.sub(r'struct([a-zA-Z_]\w*;?)?\*', "$P$", change_code)
        # Токенизация структур
        change_code = re.sub(r'(struct|union)([a-zA-Z_]\w*;?)?', "$V$", change_code)
        # Токенизация основных типов данных
        change_code = re.sub(r'({int_types}|{char_types}|{float_types}|void)\*+([a-zA-Z_]\w*;?)?'.format(
            int_types=self.__int_types, char_types=self.__char_types, float_types=self.__float_types), "$P$", change_code)
        change_code = re.sub(r'({char_types})([a-zA-Z_]\w*;?)?'.format(char_types=self.__char_types), "$B$", change_code)
        change_code = re.sub(r'({float_types})([a-zA-Z_]\w*;?)?'.format(float_types=self.__float_types), "$D$",
                             change_code)
        change_code = re.sub(r'({int_types})([a-zA-Z_]\w*;?)?'.format(int_types=self.__int_types), "$N$", change_code)
        # Токенизация циклов
        change_code = re.sub(r'do', "$S$", change_code)
        change_code = re.sub(r'while\([^;]*\);', "", change_code)
        change_code = re.sub(r'(for|while)\([^)]*\)', "$S$", change_code)
        # Токенизация управляющих конструкций
        change_code = re.sub(r'continue|break|goto', "$G$", change_code)
        # Токенизация условных конструкций
        change_code = re.sub(r'(((if|elseif)\([^)]*\))|else)', "$I$", change_code)
        # Токенизация сочетаний оператора присваивания
        change_code = re.sub(r'[+\-*/%]=', "$A$$M$", change_code)
        change_code = re.sub(r'(<<|>>|&|\^|\|)=', "$A$$U$", change_code)
        # Токенизация математических выражений
        change_code = re.sub(r'(([a-zA-Z_]\w*)\+\+)|(\+\+[a-zA-Z_]\w*)', "$M$", change_code)
        change_code = re.sub(r'(([a-zA-Z_]\w*)--)|(--[a-zA-Z_]\w*)', "$M$", change_code)
        change_code = re.sub(r'[^={},(]\*', "$M$", change_code)
        change_code = re.sub(r'[^={}><|&][+\-/%][^>]', "$M$", change_code)
        # Токенизация логических операций
        change_code = re.sub(r'&&|\|\||!', "$L$", change_code)
        # Токенизация побитовых операций
        change_code = re.sub(r'[^={}><|&](<<|>>|&|\^|\|)', "$U$", change_code)
        change_code = re.sub(r'~', "$U$", change_code)
        # Токенизация сравнений
        change_code = re.sub(r'==|([^-]>)|<|<=|>=|!=', "$E$", change_code)
        # Токенизация присваивания
        change_code = re.sub(r'=(\{[^;]*};)?', "$A$", change_code)
        # Удаление всех символов не соответствующих токенам
        # change_code = re.sub(r'\([^)$]*\)', "$()$", change_code)
        print(change_code, "\n")
        change_code = re.sub(r'[^{}NDBPCAFTMRISELUGV]*', "", change_code)

        return change_code

    def _clear_import(self, src):
        result = re.sub(r'\s*#include\s*[<"].*[>"]\s*', "", src)
        return result

    def _clear_special_characters(self, src):
        return src

    def _clear_comments(self, src):
        result = re.sub(r'//\s*.*(\n|$)', "", src)
        result = re.sub(r'//*(.|\n)*/*/', "", result)
        return result
