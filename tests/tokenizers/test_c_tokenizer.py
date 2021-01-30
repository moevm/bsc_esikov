import unittest
from src.tokenizers.c_tokenizer import CTokenizer
from src.token import Token


class TestCTokenizer(unittest.TestCase):
    def setUp(self):
        self.tokenizer = CTokenizer()
        self.switch_str = 'switch(x) { case 1: { printf("x = 1"); break; } case 2: printf("x = 2"); break; ' \
                          'default: { printf("x is undefined"); break;}}'

    def test_clear_comments(self):
        self.assertEqual(CTokenizer.clear_comments(""), "")
        self.assertEqual(CTokenizer.clear_comments("//comment"), "")
        self.assertEqual(CTokenizer.clear_comments("// comment"), "")
        self.assertEqual(CTokenizer.clear_comments("//comment\n"), "")
        self.assertEqual(CTokenizer.clear_comments("// comment\n"), "")
        self.assertEqual(CTokenizer.clear_comments("//  comment //comment"), "")
        self.assertEqual(CTokenizer.clear_comments("int x = 0; // integer x is 0"), "int x = 0; ")
        self.assertEqual(CTokenizer.clear_comments("// integer x is 0\nint x = 0;"), "int x = 0;")
        self.assertEqual(CTokenizer.clear_comments("//comment1\nint x = 0;\n// comment2"), "int x = 0;\n")
        self.assertEqual(CTokenizer.clear_comments("/*comment*/"), "")
        self.assertEqual(CTokenizer.clear_comments("/* comment */"), "")
        self.assertEqual(CTokenizer.clear_comments(" /* comment */ "), "  ")
        self.assertEqual(CTokenizer.clear_comments("/*int x = 0; float y = 1.0; */"), "")
        self.assertEqual(CTokenizer.clear_comments("/*int x = 0;\nfloat y = 1.0;\n*/"), "")
        self.assertEqual(CTokenizer.clear_comments("/*\nint x = 0;\n*/\nfloat y = 1.0;\n/*\nint x = 0;\n*/"), "\nfloat y = 1.0;\n")

    def test_replace_comments(self):
        self.assertEqual(CTokenizer.replace_comments(""), "")
        self.assertEqual(CTokenizer.replace_comments("//comment"), " " * 9)
        self.assertEqual(CTokenizer.replace_comments("// comment"), " " * 10)
        self.assertEqual(CTokenizer.replace_comments("//comment\n"), " " * 10)
        self.assertEqual(CTokenizer.replace_comments("// comment\n"), " " * 11)
        self.assertEqual(CTokenizer.replace_comments("//  comment //comment"), " " * 21)
        self.assertEqual(CTokenizer.replace_comments("int x = 0; // integer x is 0"), "int x = 0; " + " " * 17)
        self.assertEqual(CTokenizer.replace_comments("// integer x is 0\nint x = 0;"), " " * 18 + "int x = 0;")
        self.assertEqual(CTokenizer.replace_comments("//comment1\nint x = 0;\n// comment2"), " " * 11 + "int x = 0;\n" + " " * 11)
        self.assertEqual(CTokenizer.replace_comments("/*comment*/"), " " * 11)
        self.assertEqual(CTokenizer.replace_comments("/* comment */"), " " * 13)
        self.assertEqual(CTokenizer.replace_comments(" /* comment */ "), " " + " " * 13 + " ")
        self.assertEqual(CTokenizer.replace_comments("/*int x = 0; float y = 1.0; */"), " " * 30)
        self.assertEqual(CTokenizer.replace_comments("/*int x = 0;\nfloat y = 1.0;\n*/"), " " * 30)
        self.assertEqual(CTokenizer.replace_comments("/*\nint x = 0;\n*/\nfloat y = 1.0;\n/*\nint x = 0;\n*/"), " " * 16 + "\nfloat y = 1.0;\n" + " " * 16)

    def test_clear_import(self):
        self.assertEqual(CTokenizer.clear_import("#include <stdio.h>"), "")
        self.assertEqual(CTokenizer.clear_import(' #include "max.h"  '), "")
        self.assertEqual(CTokenizer.clear_import('#include <stdio.h>\n#include "max.h"'), "")
        self.assertEqual(CTokenizer.clear_import('#include <stdio.h>\n#include "max.h"\n'), "")
        self.assertEqual(CTokenizer.clear_import('#include <stdio.h>\n#include "max.h"\nint x = 0 ; \n'), "int x = 0 ; \n")

    def test_replace_import(self):
        self.assertEqual(CTokenizer.replace_import("#include <stdio.h>"), " " * 18)
        self.assertEqual(CTokenizer.replace_import(' #include "max.h"  '), " " + " " * 16 + "  ")
        self.assertEqual(CTokenizer.replace_import('#include <stdio.h>\n#include "max.h"'), " " * 18 + "\n" + " " * 16)
        self.assertEqual(CTokenizer.replace_import('#include <stdio.h>\n#include "max.h"\n'), " " * 18 + "\n" + " " * 16 + "\n")
        self.assertEqual(CTokenizer.replace_import('#include <stdio.h>\n#include "max.h"\nint x = 0 ; \n'), " " * 18 + "\n" + " " * 16 + "\nint x = 0 ; \n")

    def test_find_index_end_switch(self):
        self.assertEqual(CTokenizer.find_index_end_switch(CTokenizer.clear_space(self.switch_str)), 103)
        self.assertEqual(CTokenizer.find_index_end_switch(CTokenizer.clear_space(self.switch_str * 2)), 103)
        self.assertEqual(CTokenizer.find_index_end_switch(CTokenizer.clear_space(self.switch_str * 2), 104), 207)
        self.assertIsNone(CTokenizer.find_index_end_switch("if(a > b) return a; else a++;"))
        self.assertEqual(CTokenizer.find_index_end_switch(self.switch_str), 124)
        self.assertEqual(CTokenizer.find_index_end_switch(self.switch_str * 2), 124)
        self.assertEqual(CTokenizer.find_index_end_switch(self.switch_str * 2, 125), 249)

    def test_replace_break_in_switch(self):
        replace_str = CTokenizer.replace_break_in_switch(CTokenizer.clear_space(self.switch_str))
        self.assertEqual(replace_str.find("break;"), -1)
        replace_str = CTokenizer.replace_break_in_switch(CTokenizer.clear_space(self.switch_str * 2))
        self.assertEqual(replace_str.find("break;"), -1)
        replace_str = "while(x < 10) x += 1;"
        self.assertEqual(CTokenizer.replace_break_in_switch(replace_str), replace_str)
        replace_str = CTokenizer.replace_break_in_switch(self.switch_str)
        self.assertEqual(replace_str.find("break;"), -1)
        correct_str = 'switch(x) { case 1: { printf("x = 1"); ' + CTokenizer.NOT_TOKEN * 7 + \
                      '} case 2: printf("x = 2"); ' + CTokenizer.NOT_TOKEN * 6 + \
                      '}default: { printf("x is undefined"); ' + CTokenizer.NOT_TOKEN * 6 + '};'
        self.assertEqual(replace_str, correct_str)
        replace_str = CTokenizer.replace_break_in_switch(self.switch_str * 2)
        self.assertEqual(replace_str.find("break;"), -1)

    def test_place_curly_braces_in_src(self):
        self.assertEqual(CTokenizer.place_curly_braces_in_src("IR;"), "I{R;}")
        self.assertEqual(CTokenizer.place_curly_braces_in_src("I{R;}"), "I{R;}")
        self.assertEqual(CTokenizer.place_curly_braces_in_src("IR;IR;IR;"), "I{R;}I{R;}I{R;}")
        self.assertEqual(CTokenizer.place_curly_braces_in_src("I{R;}I{R;}I{R;}"), "I{R;}I{R;}I{R;}")
        self.assertEqual(CTokenizer.place_curly_braces_in_src("SC;"), "S{C;}")
        self.assertEqual(CTokenizer.place_curly_braces_in_src("S{C;}"), "S{C;}")
        self.assertEqual(CTokenizer.place_curly_braces_in_src("SC;"), "S{C;}")
        self.assertEqual(CTokenizer.place_curly_braces_in_src("S{C;}"), "S{C;}")
        self.assertEqual(CTokenizer.place_curly_braces_in_src("SAM;"), "S{AM;}")
        self.assertEqual(CTokenizer.place_curly_braces_in_src("S{AM;}"), "S{AM;}")
        self.assertEqual(CTokenizer.place_curly_braces_in_src("SIAM;"), "S{I{AM;}}")
        self.assertEqual(CTokenizer.place_curly_braces_in_src("S{I{AM;}}"), "S{I{AM;}}")
        self.assertEqual(CTokenizer.place_curly_braces_in_src("S{IAM;}"), "S{I{AM;}}")
        self.assertEqual(CTokenizer.place_curly_braces_in_src("SI{AM;}"), "S{I{AM;}}")
        self.assertEqual(CTokenizer.place_curly_braces_in_src("SC;SC;"), "S{C;}S{C;}")
        self.assertEqual(CTokenizer.place_curly_braces_in_src("SIAM;SIAM;"), "S{I{AM;}}S{I{AM;}}")

    def tokenize_basic_test_case(self, tokenizer):
        self.assertEqual(tokenizer("// comment"), "")
        self.assertEqual(tokenizer("#include <stdio.h>"), "")
        self.assertEqual(tokenizer("unsigned long testValue = 9999999;"), "NA")
        self.assertEqual(tokenizer("unsigned char testValue;"), "B")
        self.assertEqual(tokenizer("long double testValue;"), "D")
        self.assertEqual(tokenizer("signed char **pointer;"), "P")
        self.assertEqual(tokenizer("signed char** pointer;"), "P")
        self.assertEqual(tokenizer("signed char * * pointer;"), "P")
        self.assertEqual(tokenizer('struct person *p;'), "P")
        self.assertEqual(tokenizer("int *pointer = &value;"), "PA")
        self.assertEqual(tokenizer("int value = *ptr;"), "NA")
        self.assertEqual(tokenizer("void* voidptr = pointer;"), "PA")
        self.assertEqual(tokenizer("int *pa = NULL;"), "PA")
        self.assertEqual(tokenizer("void* voidptr = longintegers;"), "PA")
        self.assertEqual(tokenizer("void (*message) (void);"), "P")
        self.assertEqual(tokenizer("uint16_t ( *func_name_4 )( uint8_t, int16_t);"), "P")
        self.assertEqual(tokenizer("void (*message) (void) = hello;"), "PA")
        self.assertEqual(tokenizer(" void** ( *message) ( void)= hello ;"), "PA")
        self.assertEqual(tokenizer("int (*operation)(int a, int b) = add;"), "PA")
        self.assertEqual(tokenizer("void (*operations[3])(int, int) = {add, subtract, multiply};"), "PA")
        self.assertEqual(tokenizer("char * name = p_kate->name;"), "PA")
        self.assertEqual(tokenizer(" void * * ( * * message) ( void);"), "P")
        self.assertEqual(tokenizer("double (*actions[] ) (int, int);"), "P")
        self.assertEqual(tokenizer("(int)x;"), "T")
        self.assertEqual(tokenizer("( int*  *) x;"), "T")
        self.assertEqual(tokenizer("func();"), "C")
        self.assertEqual(tokenizer("func(x);"), "C")
        self.assertEqual(tokenizer(" func (  x) ; "), "C")
        self.assertEqual(tokenizer("func(a,b)\n;"), "C")
        self.assertEqual(tokenizer("func(a, sum(a, b))\n;"), "C")
        # self.assertEqual(tokenizer("void *message (void);"), "PC")
        self.assertEqual(tokenizer('printf("sizeof(number) = %d \n", sizeof(number));'), "C")
        self.assertEqual(tokenizer("int printf(const char* format, ...);"), "C")
        self.assertEqual(tokenizer('addminutes(p_time, 21);'), "C")
        self.assertEqual(tokenizer("int value = function();"), "NAC")
        self.assertEqual(tokenizer("int value = function(a, b, c);"), "NAC")
        self.assertEqual(tokenizer("float x = 0.456; double value = (double)x;"), "DADAT")
        self.assertEqual(tokenizer("i++"), "M")
        self.assertEqual(tokenizer("--i;"), "M")
        self.assertEqual(tokenizer("int *ptr = &n; ptr++;"), "PAM")
        self.assertEqual(tokenizer("char * name = p_kate->name++;"), "PAM")
        self.assertEqual(tokenizer("int value = 45 + 94;"), "NAM")
        self.assertEqual(tokenizer("int value = 45 * 94;"), "NAM")
        self.assertEqual(tokenizer("int value = T;"), "NA")
        self.assertEqual(tokenizer("int value = T + A;"), "NAM")
        self.assertEqual(tokenizer("int d = -435;"), "NA")
        self.assertEqual(tokenizer("int age = (*p_kate).age;"), "NA")
        self.assertEqual(tokenizer("int age = (*p_kate).age * (*p_kate).age;"), "NAM")
        self.assertEqual(tokenizer("int *pd = (int *)pc;"), "PAT")
        self.assertEqual(tokenizer("int numbers[4]; numbers[0] = 1;"), "NA")
        self.assertEqual(tokenizer("float numbers[4][4] = 9.0;"), "DA")
        self.assertEqual(tokenizer("int numbers[] = { 1, 2, 3, 5 };"), "NA")
        self.assertEqual(tokenizer("int numbers[3][2] = { {1, 2}, {4, 5}, {7, 8} };"), "NA")
        self.assertEqual(tokenizer('char welcome[] = "Hello";'), "BA")
        self.assertEqual(tokenizer("char welcome[] = {'H', 'e', 'l', 'l', 'o', '\0'};"), "BA")
        self.assertEqual(tokenizer("int *p2[] = { &a[1], &a[2], &a[0] };"), "PA")
        self.assertEqual(tokenizer('tom.age = 23;'), "A")
        self.assertEqual(tokenizer('tom.age = alex.age;'), "A")
        self.assertEqual(tokenizer('phone.manufacturer.name = "Alex";'), "A")
        self.assertEqual(tokenizer('p_kate->name = "Tom";'), "A")
        self.assertEqual(tokenizer('age = people[i].name'), "A")
        self.assertEqual(tokenizer('age = *(people[i]->name)'), "A")
        self.assertEqual(tokenizer("static int i = 0;"), "NA")
        self.assertEqual(tokenizer("const float PI = 3.14;"), "DA")
        self.assertEqual(tokenizer("float *const ptr=&i;"), "PA")
        self.assertEqual(tokenizer("const float *const ptr=&i;"), "PA")
        self.assertEqual(tokenizer("float a = 10.0 / 4;"), "DAM")
        self.assertEqual(tokenizer("int value = 45 + func(a, b);"), "NAMC")
        self.assertEqual(tokenizer("int value = (45 + 94) / 4;"), "NAMM")
        self.assertEqual(tokenizer("return a * b;"), "RM")
        self.assertEqual(tokenizer("return func();"), "RC")
        self.assertEqual(tokenizer("return;"), "R")
        self.assertEqual(tokenizer("\nreturn;"), "R")
        self.assertEqual(tokenizer(";return   ;"), "R")
        self.assertEqual(tokenizer("array[0] = 10 % 2;"), "AM")
        self.assertEqual(tokenizer("void* value = func(T, A, X);"), "PAC")
        self.assertEqual(tokenizer('struct time * p_time = input();'), "PAC")
        self.assertEqual(tokenizer("int x, y, z; x = y = z = 0;"), "NAAA")
        self.assertEqual(tokenizer("a = b = c = 34 + 7;"), "AAAM")
        self.assertEqual(tokenizer("double e = (double)a / (double)b;"), "DATMT")
        self.assertEqual(tokenizer("int sum(int a, int b) {"), "F{")
        self.assertEqual(tokenizer("void  _sum (){"), "F{")
        self.assertEqual(tokenizer(" int **  _sum (int a[]){"), "F{")
        self.assertEqual(tokenizer("int* sum(int* n){"), "F{")
        self.assertEqual(tokenizer("int (*select(void))(void){"), "F{")
        self.assertEqual(tokenizer("int* (*select ( )) ( ) {"), "F{")
        self.assertEqual(tokenizer("int** (*select ( )) ( ) {"), "F{")
        self.assertEqual(tokenizer("int operation(int (*op)(int, int), int a, int b){"), "F{")
        self.assertEqual(tokenizer("int sum(int n, ...){"), "F{")
        self.assertEqual(tokenizer("int* sum(int n, ...){"), "F{")
        self.assertEqual(tokenizer("void action(int (*condition)(int), int number, int n){"), "F{")
        self.assertEqual(tokenizer('struct time addminutes(struct time t, int minutes){'), "F{")
        self.assertEqual(tokenizer('struct time * addminutes(struct time * t, int minutes){'), "F{")
        self.assertEqual(tokenizer("int sum(int a, int b) { return a + b; }"), "F{RM}")
        self.assertEqual(tokenizer('void display(register int a){printf("a=%d \n", a);}'), "F{C}")
        self.assertEqual(tokenizer('void addminutes(struct time *t, int minutes){'), "F{")
        self.assertEqual(tokenizer('struct time * input(){'), "F{")
        self.assertEqual(tokenizer("int c = !2;"), "NAL")
        self.assertEqual(tokenizer("int d = 0 && 7;"), "NAL")
        self.assertEqual(tokenizer("int e = 0 || 0;"), "NAL")
        self.assertEqual(tokenizer("int d = a && b || c;"), "NALL")
        self.assertEqual(tokenizer("int a = 2 << 2;"), "NAU")
        self.assertEqual(tokenizer("int a = 5 | 2;"), "NAU")
        self.assertEqual(tokenizer("int b = 6 & 2;"), "NAU")
        self.assertEqual(tokenizer("int c = 5 ^ 2;"), "NAU")
        self.assertEqual(tokenizer("int d = ~9;"), "NAU")
        self.assertEqual(tokenizer("a <<= 4;"), "AU")
        self.assertEqual(tokenizer("a |= 4;"), "AU")
        self.assertEqual(tokenizer("a &= 4;"), "AU")
        self.assertEqual(tokenizer("a ^= 4;"), "AU")
        self.assertEqual(tokenizer("a += 4;"), "AM")
        self.assertEqual(tokenizer("a -= 4;"), "AM")
        self.assertEqual(tokenizer("a *= 4;"), "AM")
        self.assertEqual(tokenizer("a /= 4;"), "AM")
        self.assertEqual(tokenizer("a %= 4;"), "AM")
        self.assertEqual(tokenizer("int c = a == b;"), "NAE")
        self.assertEqual(tokenizer("int d = -2 > -5 && 0 < 7 || 0 == 0;"), "NAELELE")
        self.assertEqual(tokenizer("struct person tom;"), "V")
        self.assertEqual(tokenizer("struct person { int age; char * name; };"), "V{NP}")
        self.assertEqual(tokenizer('struct person tom = {23, "Tom"};'), "VA")
        self.assertEqual(tokenizer("struct person { int age; char * name; } tom, bob, alice;"), "V{NP}")
        self.assertEqual(tokenizer("struct { int age; char * name; } tom, bob, alice;"), "V{NP}")
        self.assertEqual(tokenizer("struct smartphone {char title[20]; int price; struct company manufacturer;};"), "V{BNV}")
        self.assertEqual(tokenizer("struct person { int age; char name[20]; } *p1, *p2;"), "V{NB}")
        self.assertEqual(tokenizer('struct person people[] = {23, "Tom", 32, "Bob", 26, "Alice", 41, "Sam"};'), "VA")
        self.assertEqual(tokenizer('struct time result_time = addminutes(current_time, minutes);'), "VAC")
        self.assertEqual(tokenizer('union code id = {120};'), "VA")
        self.assertEqual(tokenizer('union code { int digit; char letter; };'), "V{NB}")
        # self.assertEqual(tokenizer('struct point{ unsigned int x:5; unsigned int y:3;};'), "V{NN}")
        self.assertEqual(tokenizer("if (a > b) return a; else return b;"), "I{R}I{R}")
        # self.assertEqual(tokenizer("if ((a > b) && (c > b)) return a; else return b;"), "I{R}I{R}")
        self.assertEqual(tokenizer("if(c > b) return c; else if(b < c) return b; else return 0;"), "I{R}I{R}I{R}")
        self.assertEqual(tokenizer("if(func(a, b)) return a;"), "I{R}")
        self.assertEqual(tokenizer("if(func(a, b)){ a += b; return a;}"), "I{AMR}")
        self.assertEqual(tokenizer("if (a > b) { a++; return a;} else { b++; return b; }"), "I{MR}I{MR}")
        self.assertEqual(tokenizer('if (i % 2 == 0) continue;'), "I{G}")
        self.assertEqual(tokenizer('if (i > 10) break;'), "I{G}")
        self.assertEqual(tokenizer('do i--; while (i > 0);'), "S{M}")
        self.assertEqual(tokenizer('do if (i > 10) i--; while (i > 0);'), "S{I{M}}")
        self.assertEqual(tokenizer('do if (i > 10) break; while (i > 0);'), "S{I{G}}")
        self.assertEqual(tokenizer("while(x < 10) x += 1;"), "S{AM}")
        self.assertEqual(tokenizer("for(int i = 0; i < 10; i++) compare(func(i), 0);"), "S{C}")
        self.assertEqual(tokenizer("if(x < 10) int a;"), "I{N}")
        # self.assertEqual(tokenizer("if(x < 10) int a = 10;"), "I{NA}")
        # self.assertEqual(tokenizer("if(x < 10) if(x % 2 == 0) y += x;"), "I{I{AM}}")
        # self.assertEqual(tokenizer("while(x < 10) if(x % 2 == 0) y += x;"), "S{I{AM}}")
        # self.assertEqual(tokenizer("while(x = func(x)) if(x % 2 == 0) y += x;"), "S{I{AM}}")
        # self.assertEqual(tokenizer("while(x < 10) if(x % 2 == 0) y += x; else return 0;"), "SIAMIR")
        # self.assertEqual(self.tokenizer.tokenize("z = (x > y) ? x: y;"), "IAIA")
        # self.assertEqual(self.tokenizer.tokenize("z = (x > y) ? func1(): func2();"), "IACIAC")
        # self.assertEqual(self.tokenizer.tokenize("(x > y) ? func1(): func2();"), "ICIC")
        self.assertEqual(tokenizer(self.switch_str), "I{C}I{C}I{C}")

    def test_fast_tokenize(self):
        self.tokenize_basic_test_case(self.tokenizer.fast_tokenize)

    def test_tokenize(self):
        self.tokenize_basic_test_case(self.tokenize_runner)

    def tokenize_runner(self, src):
        tokens = self.tokenizer.tokenize(src)
        return Token.get_tokens_str_from_token_list(tokens)

    def assert_tokens_list(self, current, true):
        self.assertEqual(len(current), len(true))
        for i in range(len(current)):
            self.assertEqual(current[i].symbol, true[i].symbol)
            self.assertEqual(current[i].start, true[i].start)
            self.assertEqual(current[i].end, true[i].end)

    def test_place_curly_braces_in_tokens_list(self):
        tokens = [
            Token("I", 0, 1),
            Token("M", 3, 10)
        ]
        true_result = [
            Token("I", 0, 1),
            Token("{", 1, 1),
            Token("M", 3, 10),
            Token("}", 10, 10)
        ]
        current_result = CTokenizer.place_curly_braces_in_tokens_list(tokens)
        self.assert_tokens_list(current_result, true_result)

        tokens = [
            Token("S", 0, 1),
            Token("M", 3, 10)
        ]
        true_result = [
            Token("S", 0, 1),
            Token("{", 1, 1),
            Token("M", 3, 10),
            Token("}", 10, 10)
        ]
        current_result = CTokenizer.place_curly_braces_in_tokens_list(tokens)
        self.assert_tokens_list(current_result, true_result)

        tokens = [
            Token("S", 0, 1),
            Token("I", 3, 10),
            Token("M", 12, 15)
        ]
        true_result = [
            Token("S", 0, 1),
            Token("{", 1, 1),
            Token("I", 3, 10),
            Token("{", 4, 10),
            Token("M", 12, 15),
            Token("}", 15, 15),
            Token("}", 15, 15)
        ]
        current_result = CTokenizer.place_curly_braces_in_tokens_list(tokens)
        self.assert_tokens_list(current_result, true_result)

        tokens = [
            Token("I", 0, 1),
            Token("M", 3, 10),
            Token("I", 12, 15),
            Token("R", 17, 20)
        ]
        true_result = [
            Token("I", 0, 1),
            Token("{", 1, 1),
            Token("M", 3, 10),
            Token("}", 10, 10),
            Token("I", 12, 15),
            Token("{", 13, 15),
            Token("R", 17, 20),
            Token("}", 20, 20)
        ]
        current_result = CTokenizer.place_curly_braces_in_tokens_list(tokens)
        self.assert_tokens_list(current_result, true_result)

        tokens = [
            Token("I", 0, 1),
            Token("{", 2, 2),
            Token("M", 3, 10),
            Token("}", 10, 10)
        ]
        current_result = CTokenizer.place_curly_braces_in_tokens_list(tokens)
        self.assert_tokens_list(current_result, tokens)

        tokens = [
            Token("I", 0, 1),
            Token("{", 2, 2),
            Token("M", 3, 10),
            Token("R", 14, 20),
            Token("}", 21, 21)
        ]
        current_result = CTokenizer.place_curly_braces_in_tokens_list(tokens)
        self.assert_tokens_list(current_result, tokens)


if __name__ == '__main__':
    unittest.main()