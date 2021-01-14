import unittest
from src.tokenizers.c_tokenizer import CTokenizer


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

    def test_clear_import(self):
        self.assertEqual(CTokenizer.clear_import("#include <stdio.h>"), "")
        self.assertEqual(CTokenizer.clear_import(' #include "max.h"  '), "")
        self.assertEqual(CTokenizer.clear_import('#include <stdio.h>\n#include "max.h"'), "")
        self.assertEqual(CTokenizer.clear_import('#include <stdio.h>\n#include "max.h"\n'), "")
        self.assertEqual(CTokenizer.clear_import('#include <stdio.h>\n#include "max.h"\nint x = 0 ; \n'), "int x = 0 ; \n")

    def test_tokenize_base_case(self):
        self.assertEqual(self.tokenizer.tokenize("// comment"), "")
        self.assertEqual(self.tokenizer.tokenize("#include <stdio.h>"), "")
        self.assertEqual(self.tokenizer.tokenize("unsigned long testValue = 9999999;"), "NA")
        self.assertEqual(self.tokenizer.tokenize("unsigned char testValue;"), "B")
        self.assertEqual(self.tokenizer.tokenize("long double testValue;"), "D")
        self.assertEqual(self.tokenizer.tokenize("signed char **pointer;"), "P")
        self.assertEqual(self.tokenizer.tokenize("int *pointer = &value;"), "PA")
        self.assertEqual(self.tokenizer.tokenize("int value = *ptr;"), "NA")
        self.assertEqual(self.tokenizer.tokenize("void* voidptr = pointer;"), "PA")
        self.assertEqual(self.tokenizer.tokenize("void* voidptr = longintegers;"), "PA")
        self.assertEqual(self.tokenizer.tokenize("int value = function();"), "NAC")
        self.assertEqual(self.tokenizer.tokenize("int value = function(a, b, c);"), "NAC")
        self.assertEqual(self.tokenizer.tokenize("float x = 0.456; double value = (double)x;"), "DADAT")
        self.assertEqual(self.tokenizer.tokenize("i++"), "M")
        self.assertEqual(self.tokenizer.tokenize("--i;"), "M")
        self.assertEqual(self.tokenizer.tokenize("int value = 45 + 94;"), "NAM")
        self.assertEqual(self.tokenizer.tokenize("int value = 45 + func(a, b);"), "NAMC")
        self.assertEqual(self.tokenizer.tokenize("int value = (45 + 94) / 4;"), "NAMM")
        self.assertEqual(self.tokenizer.tokenize("return a * b;"), "RM")
        self.assertEqual(self.tokenizer.tokenize("return func();"), "RC")
        self.assertEqual(self.tokenizer.tokenize("return;"), "R")
        self.assertEqual(self.tokenizer.tokenize("int sum(int a, int b) { return a + b; }"), "F{RM}")
        self.assertEqual(self.tokenizer.tokenize("array[0] = 10 % 2;"), "AM")
        self.assertEqual(self.tokenizer.tokenize("int x, y, z; x = y = z = 0;"), "NAAA")
        self.assertEqual(self.tokenizer.tokenize("if(a > b) return a; else a++;"), "I{R}I{M}")
        self.assertEqual(self.tokenizer.tokenize("if(c > b) return c; else if(b < c) return b; else return 0;"), "I{R}I{R}I{R}")
        self.assertEqual(self.tokenizer.tokenize("if(func(a, b)) return a;"), "I{R}")
        # self.assertEqual(self.tokenizer.tokenize("z = (x > y) ? x: y;"), "IAIA")
        # self.assertEqual(self.tokenizer.tokenize("z = (x > y) ? func1(): func2();"), "IACIAC")
        # self.assertEqual(self.tokenizer.tokenize("(x > y) ? func1(): func2();"), "ICIC")
        self.assertEqual(self.tokenizer.tokenize("int value = T;"), "NA")
        self.assertEqual(self.tokenizer.tokenize("int value = T + A;"), "NAM")
        self.assertEqual(self.tokenizer.tokenize("void* value = func(T, A, X);"), "PAC")
        self.assertEqual(self.tokenizer.tokenize("while(x < 10) x += 1;"), "S{AM}")
        self.assertEqual(self.tokenizer.tokenize("for(int i = 0; i < 10; i++) compare(func(i), 0);"), "S{C}")
        self.assertEqual(self.tokenizer.tokenize("while(x < 10) if(x % 2 == 0) y += x;"), "S{I{AM}}")
        self.assertEqual(self.tokenizer.tokenize("while(x = func(x)) if(x % 2 == 0) y += x;"), "S{I{AM}}")
        # self.assertEqual(self.tokenizer.tokenize("while(x < 10) if(x % 2 == 0) y += x; else return 0;"), "SIAMIR")
        self.assertEqual(self.tokenizer.tokenize('do i--; while (i > 0);'), "S{M}")
        self.assertEqual(self.tokenizer.tokenize('do if (i > 10) break; while (i > 0);'), "S{I{G}}")
        self.assertEqual(self.tokenizer.tokenize('if (i % 2 == 0) continue;'), "I{G}")
        self.assertEqual(self.tokenizer.tokenize('if (i > 10) break;'), "I{G}")
        self.assertEqual(self.tokenizer.tokenize('printf("sizeof(number) = %d \n", sizeof(number));'), "C")
        self.assertEqual(self.tokenizer.tokenize("const float PI = 3.14;"), "DA")
        self.assertEqual(self.tokenizer.tokenize("float a = 10.0 / 4;"), "DAM")
        self.assertEqual(self.tokenizer.tokenize("a = b = c = 34 + 7;"), "AAAM")
        self.assertEqual(self.tokenizer.tokenize("double e = (double)a / (double)b;"), "DATMT")
        self.assertEqual(self.tokenizer.tokenize("int c = a == b;"), "NAE")
        self.assertEqual(self.tokenizer.tokenize("int c = !2;"), "NAL")
        self.assertEqual(self.tokenizer.tokenize("int d = 0 && 7;"), "NAL")
        self.assertEqual(self.tokenizer.tokenize("int e = 0 || 0;"), "NAL")
        self.assertEqual(self.tokenizer.tokenize("int d = a && b || c;"), "NALL")
        self.assertEqual(self.tokenizer.tokenize("int d = -435;"), "NA")
        self.assertEqual(self.tokenizer.tokenize("int d = -2 > -5 && 0 < 7 || 0 == 0;"), "NAELELE")
        self.assertEqual(self.tokenizer.tokenize("int a = 2 << 2;"), "NAU")
        self.assertEqual(self.tokenizer.tokenize("int a = 5 | 2;"), "NAU")
        self.assertEqual(self.tokenizer.tokenize("int b = 6 & 2;"), "NAU")
        self.assertEqual(self.tokenizer.tokenize("int c = 5 ^ 2;"), "NAU")
        self.assertEqual(self.tokenizer.tokenize("int d = ~9;"), "NAU")
        self.assertEqual(self.tokenizer.tokenize("a <<= 4;"), "AU")
        self.assertEqual(self.tokenizer.tokenize("a |= 4;"), "AU")
        self.assertEqual(self.tokenizer.tokenize("a &= 4;"), "AU")
        self.assertEqual(self.tokenizer.tokenize("a ^= 4;"), "AU")
        self.assertEqual(self.tokenizer.tokenize('void display(register int a){printf("a=%d \n", a);}'), "F{C}")
        self.assertEqual(self.tokenizer.tokenize("static int i = 0;"), "NA")
        self.assertEqual(self.tokenizer.tokenize("int *pa = NULL;"), "PA")
        self.assertEqual(self.tokenizer.tokenize("int *pd = (int *)pc;"), "PAT")
        self.assertEqual(self.tokenizer.tokenize("int *ptr = &n; ptr++;"), "PAM")
        self.assertEqual(self.tokenizer.tokenize("const int *pa = &a;"), "PA")
        self.assertEqual(self.tokenizer.tokenize("int *const pa = &a;"), "PA")
        self.assertEqual(self.tokenizer.tokenize("const int *const pa = &a;"), "PA")
        self.assertEqual(self.tokenizer.tokenize("void (*message) (void);"), "P")
        self.assertEqual(self.tokenizer.tokenize("void* (*message) (void);"), "P")
        self.assertEqual(self.tokenizer.tokenize("void *message (void);"), "PC")
        self.assertEqual(self.tokenizer.tokenize("uint16_t ( *func_name_4 )( uint8_t, int16_t);"), "P")
        self.assertEqual(self.tokenizer.tokenize("int (*operation)(int a, int b) = add;"), "PA")
        self.assertEqual(self.tokenizer.tokenize("void action(int (*condition)(int), int number, int n){"), "F{")
        self.assertEqual(self.tokenizer.tokenize("int (*select(void))(void){"), "F{")
        self.assertEqual(self.tokenizer.tokenize("int* (*select(void))(void){"), "F{")
        self.assertEqual(self.tokenizer.tokenize("int sum(int n, ...){"), "F{")
        self.assertEqual(self.tokenizer.tokenize("int printf(const char* format, ...);"), "C")
        self.assertEqual(self.tokenizer.tokenize("int* sum(int n, ...){"), "F{")
        self.assertEqual(self.tokenizer.tokenize("int numbers[4]; numbers[0] = 1;"), "NA")
        self.assertEqual(self.tokenizer.tokenize("int numbers[] = { 1, 2, 3, 5 };"), "NA")
        self.assertEqual(self.tokenizer.tokenize("int numbers[3][2] = { {1, 2}, {4, 5}, {7, 8} };"), "NA")
        self.assertEqual(self.tokenizer.tokenize('char welcome[] = "Hello";'), "BA")
        self.assertEqual(self.tokenizer.tokenize("char welcome[] = {'H', 'e', 'l', 'l', 'o', '\0'};"), "BA")
        self.assertEqual(self.tokenizer.tokenize("int *p2[] = { &a[1], &a[2], &a[0] };"), "PA")
        self.assertEqual(self.tokenizer.tokenize("double (*actions[]) (int, int)"), "P")
        self.assertEqual(self.tokenizer.tokenize("void (*operations[3])(int, int) = {add, subtract, multiply};"), "PA")
        self.assertEqual(self.tokenizer.tokenize("int* sum(int[] n){"), "F{")
        self.assertEqual(self.tokenizer.tokenize("int* sum(int* n){"), "F{")
        self.assertEqual(self.tokenizer.tokenize("struct person { int age; char * name; };"), "V{NP}")
        self.assertEqual(self.tokenizer.tokenize("struct person tom;"), "V")
        self.assertEqual(self.tokenizer.tokenize('struct person tom = {23, "Tom"};'), "VA")
        self.assertEqual(self.tokenizer.tokenize('tom.age = 23;'), "A")
        self.assertEqual(self.tokenizer.tokenize('tom.age = alex.age;'), "A")
        self.assertEqual(self.tokenizer.tokenize("struct person { int age; char * name; } tom, bob, alice;"), "V{NP}")
        self.assertEqual(self.tokenizer.tokenize("struct { int age; char * name; } tom, bob, alice;"), "V{NP}")
        self.assertEqual(self.tokenizer.tokenize("struct smartphone {char title[20]; int price; struct company manufacturer;};"), "V{BNV}")
        self.assertEqual(self.tokenizer.tokenize('phone.manufacturer.name = "Alex";'), "A")
        self.assertEqual(self.tokenizer.tokenize('struct person *p;'), "P")
        self.assertEqual(self.tokenizer.tokenize("struct person { int age; char name[20]; } *p1, *p2;"), "V{NB}")
        self.assertEqual(self.tokenizer.tokenize("char * name = p_kate->name;"), "PA")
        self.assertEqual(self.tokenizer.tokenize("int age = (*p_kate).age;"), "NA")
        self.assertEqual(self.tokenizer.tokenize("char * name = p_kate->name++;"), "PAM")
        self.assertEqual(self.tokenizer.tokenize("int age = (*p_kate).age * (*p_kate).age;"), "NAM")
        self.assertEqual(self.tokenizer.tokenize('p_kate->name = "Tom";'), "A")
        self.assertEqual(self.tokenizer.tokenize('struct person people[] = {23, "Tom", 32, "Bob", 26, "Alice", 41, "Sam"};'), "VA")
        self.assertEqual(self.tokenizer.tokenize('age = people[i].name'), "A")
        self.assertEqual(self.tokenizer.tokenize('age = *(people[i]->name)'), "A")
        self.assertEqual(self.tokenizer.tokenize('struct time addminutes(struct time t, int minutes){'), "F{")
        self.assertEqual(self.tokenizer.tokenize('struct time result_time = addminutes(current_time, minutes);'), "VAC")
        self.assertEqual(self.tokenizer.tokenize('void addminutes(struct time *t, int minutes){'), "F{")
        self.assertEqual(self.tokenizer.tokenize('addminutes(p_time, 21);'), "C")
        self.assertEqual(self.tokenizer.tokenize('struct time * input(){'), "F{")
        self.assertEqual(self.tokenizer.tokenize('struct time * p_time = input();'), "PAC")
        self.assertEqual(self.tokenizer.tokenize('union code id = {120};'), "VA")
        self.assertEqual(self.tokenizer.tokenize('union code { int digit; char letter; };'), "V{NB}")
        self.assertEqual(self.tokenizer.tokenize('struct point{ unsigned int x:5; unsigned int y:3;};'), "V{NN}")
        self.assertEqual(self.tokenizer.tokenize(self.switch_str), "I{C}I{C}I{C}")

    def test_find_index_end_switch(self):
        self.assertEqual(CTokenizer.find_index_end_switch(CTokenizer.clear_space(self.switch_str)), 103)
        self.assertEqual(CTokenizer.find_index_end_switch(CTokenizer.clear_space(self.switch_str * 2)), 103)
        self.assertEqual(CTokenizer.find_index_end_switch(CTokenizer.clear_space(self.switch_str * 2), 104), 207)
        self.assertIsNone(CTokenizer.find_index_end_switch("if(a > b) return a; else a++;"))

    def test_replace_break_in_switch(self):
        replace_str = CTokenizer.replace_break_in_switch(CTokenizer.clear_space(self.switch_str))
        self.assertEqual(replace_str.find("break;"), -1)
        replace_str = CTokenizer.replace_break_in_switch(CTokenizer.clear_space(self.switch_str * 2))
        self.assertEqual(replace_str.find("break;"), -1)
        replace_str = "while(x < 10) x += 1;"
        self.assertEqual(CTokenizer.replace_break_in_switch(replace_str), replace_str)

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


if __name__ == '__main__':
    unittest.main()
