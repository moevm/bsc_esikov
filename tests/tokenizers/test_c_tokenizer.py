import unittest
from operator import attrgetter
from src.tokenizers.c_tokenizer import CTokenizer
from src.models.token import Token


class TestCTokenizer(unittest.TestCase):
    def setUp(self):
        self.tokenizer = CTokenizer()
        self.switch_str = 'switch(x) { case 1: { printf("x = 1"); break; } case 2: printf("x = 2"); break; ' \
                          'default: { printf("x is undefined"); break;}}'

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

    def test_replace_import(self):
        self.assertEqual(CTokenizer.replace_import("#include <stdio.h>"), " " * 18)
        self.assertEqual(CTokenizer.replace_import(' #include "max.h"  '), " " + " " * 16 + "  ")
        self.assertEqual(CTokenizer.replace_import('#include <stdio.h>\n#include "max.h"'), " " * 18 + "\n" + " " * 16)
        self.assertEqual(CTokenizer.replace_import('#include <stdio.h>\n#include "max.h"\n'), " " * 18 + "\n" + " " * 16 + "\n")
        self.assertEqual(CTokenizer.replace_import('#include <stdio.h>\n#include "max.h"\nint x = 0 ; \n'), " " * 18 + "\n" + " " * 16 + "\nint x = 0 ; \n")

    def test_replace_strings(self):
        self.assertEqual(CTokenizer.replace_strings("int abcd = 1000;"), "int abcd = 1000;")
        self.assertEqual(CTokenizer.replace_strings("if (p[i] == ';')"), "if (p[i] == " + CTokenizer.SUBSTITUTE * 3 + ")")
        self.assertEqual(CTokenizer.replace_strings("if ((p[i] == '.') || (p[i] == '?') || (p[i] == ';'))"), "if ((p[i] == " + CTokenizer.SUBSTITUTE * 3 + ") || (p[i] == " + CTokenizer.SUBSTITUTE * 3 + ") || (p[i] == " + CTokenizer.SUBSTITUTE * 3 + "))")
        self.assertEqual(CTokenizer.replace_strings('char* string = "abcdefgh"'), 'char* string = ' + CTokenizer.SUBSTITUTE * 10)

    def test_replace_macros(self):
        self.assertEqual(CTokenizer.replace_macros("#define N 22"), " " * 12)
        self.assertEqual(CTokenizer.replace_macros("#   define    N   22  "), " " * 22)
        self.assertEqual(CTokenizer.replace_macros("#include <stdio.h>\n#define N 22\nint a = 10;"), "#include <stdio.h>\n" + " " * 12 + "\nint a = 10;")

    def get_tokens_str_after_tokenize(self, src):
        tokens = self.tokenizer.tokenize(src)
        return Token.get_tokens_str_from_token_list(tokens)

    def test_tokenize(self):
        tokenizer = self.get_tokens_str_after_tokenize
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
        self.assertEqual(tokenizer("char* name = (char*)malloc(80*sizeof(char));"), "PATC")
        self.assertEqual(tokenizer("; func();"), "C")
        self.assertEqual(tokenizer(";func(x);"), "C")
        self.assertEqual(tokenizer("{ func (  x) ; "), "{C")
        self.assertEqual(tokenizer("}func(a,b)\n;"), "}C")
        self.assertEqual(tokenizer(";\n\t\tfunc(a == b);"), "C")
        self.assertEqual(tokenizer(":func(a, sum(a, b))\n;"), "C")
        # self.assertEqual(tokenizer("void *message (void);"), "PC")
        self.assertEqual(tokenizer('return printf("sizeof(number) = %d \n", sizeof(number));'), "RC")
        self.assertEqual(tokenizer("int printf(const char* format, ...);"), "C")  # ?????
        self.assertEqual(tokenizer('; addminutes(p_time, 21);'), "C")
        self.assertEqual(tokenizer("a = getchar();"), "AC")
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
        self.assertEqual(tokenizer('age = people[i].name;'), "A")
        self.assertEqual(tokenizer('age = *(people[i]->name);'), "A")
        self.assertEqual(tokenizer("*pa = NULL;"), "A")
        self.assertEqual(tokenizer("*input = '\0';"), "A")
        self.assertEqual(tokenizer("text[i++] = a;"), "MA")
        self.assertEqual(tokenizer("*(sentence + i) = symbol;"), "MA")
        self.assertEqual(tokenizer("*(text++) = symbol;"), "MA")
        self.assertEqual(tokenizer("*(result++) = *(text++);"), "MAM")
        self.assertEqual(tokenizer("static int i = 0;"), "NA")
        self.assertEqual(tokenizer("const float PI = 3.14;"), "DA")
        self.assertEqual(tokenizer("float *const ptr=&i;"), "PA")
        self.assertEqual(tokenizer("const float *const ptr=&i;"), "PA")
        self.assertEqual(tokenizer("float a = 10.0 / 4;"), "DAM")
        self.assertEqual(tokenizer("int value = 45 + func(a, b);"), "NAM")
        self.assertEqual(tokenizer("int value = func(y) + x;"), "NAM")
        self.assertEqual(tokenizer("int value = x + y - 2;"), "NAMM")
        self.assertEqual(tokenizer("int value = (45 + 94) / 4;"), "NAMM")
        self.assertEqual(tokenizer("int value = (45 * 94) * 4;"), "NAMM")
        self.assertEqual(tokenizer("return a * b;"), "RM")
        self.assertEqual(tokenizer("return a + b % 10;"), "RMM")
        self.assertEqual(tokenizer("return func();"), "RC")
        self.assertEqual(tokenizer("return;"), "R")
        self.assertEqual(tokenizer("\nreturn;"), "R")
        self.assertEqual(tokenizer(";return   ;"), "R")
        self.assertEqual(tokenizer("return *ptr;"), "R")
        self.assertEqual(tokenizer("return 1;"), "R")
        self.assertEqual(tokenizer("return -1;"), "R")
        self.assertEqual(tokenizer("array[0] = 10 % 2;"), "AM")
        self.assertEqual(tokenizer("void* value = func(T, A, X);"), "PAC")
        self.assertEqual(tokenizer('struct time * p_time = input();'), "PAC")
        self.assertEqual(tokenizer("int i, p;"), "N")
        self.assertEqual(tokenizer("int  i, result = 1;"), "NA")
        self.assertEqual(tokenizer("int kode, mass[20], m, count = 0;"), "NA")
        self.assertEqual(tokenizer("int i = 0, factor = 1, n = 0, m = 10 + 3, SpaceBeforeTheFirstSentence = 0;"), "NAAAAMA")
        # self.assertEqual(tokenizer("int multi_b_a = 19 + x * 3, y = foo(mass, size), z = foo(mass, size);"), "NAMMACAC")
        self.assertEqual(tokenizer("int x, y, z; x = y = z = 0;"), "NAAA")
        self.assertEqual(tokenizer("a = b = c = 34 + 7;"), "AAAM")
        self.assertEqual(tokenizer("char *text, *text1, *sentence, *MrCheck;"), "P")
        self.assertEqual(tokenizer("void * const text1, **const    text2;"), "P")
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
        self.assertEqual(tokenizer('struct point{ unsigned int x:5; unsigned int y:3;};'), "V{NN}")
        self.assertEqual(tokenizer("if (a > b) return a; else return b;"), "I{R}I{R}")
        self.assertEqual(tokenizer("if ((a > b) && (c > b)) return a; else return b;"), "I{R}I{R}")
        # self.assertEqual(tokenizer("if(c > b) return c; else if(b < c) return b; else return 0;"), "I{R}I{R}I{R}")
        self.assertEqual(tokenizer("if(func(a, b)) return a;"), "I{R}")
        self.assertEqual(tokenizer("if(func(a, b)){ a += b; return a;}"), "I{AMR}")
        self.assertEqual(tokenizer("if (a > b) { a++; return a;} else { b++; return b; }"), "I{MR}I{MR}")
        self.assertEqual(tokenizer('if (i % 2 == 0) continue;'), "I{G}")
        self.assertEqual(tokenizer('if (i > 10) break;'), "I{G}")
        self.assertEqual(tokenizer('do i--; while (i > 0);'), "S{M}")
        self.assertEqual(tokenizer('do if (i > 10) i--; while (i > 0);'), "S{I{M}}")
        self.assertEqual(tokenizer('do if (i > 10) break; while (i > 0);'), "S{I{G}}")
        self.assertEqual(tokenizer("while(x < 10) x += 1;"), "S{AM}")
        self.assertEqual(tokenizer('while((strstr(text, "Dragon flew away!") == NULL)) { foo(); }'), "S{C}")
        self.assertEqual(tokenizer("while ((str[i]==' ')||(str[i]=='\t')||(str[i]=='\n')) getchar();"), "S{C}")
        self.assertEqual(tokenizer("for(int i = 0; i < 10; i++) compare(func(i), 0);"), "S{C}")
        self.assertEqual(tokenizer("if(x < 10) int a;"), "I{N}")
        self.assertEqual(tokenizer("if(x < 10) int a = 10;"), "I{NA}")
        self.assertEqual(tokenizer("if(x < 10) if(x % 2 == 0) y += x;"), "I{I{AM}}")
        self.assertEqual(tokenizer("if (a == ';' || a == '.') { i++; }"), "I{M}")
        self.assertEqual(tokenizer("while(x < 10) if(x % 2 == 0) y += x;"), "S{I{AM}}")
        self.assertEqual(tokenizer("while(x = func(x)) if(x % 2 == 0) y += x;"), "S{I{AM}}")
        self.assertEqual(tokenizer("while(x < 10) if(x % 2 == 0) y += x; else return 0;"), "S{I{AM}I{R}}")
        self.assertEqual(tokenizer('do { printf("Hello world! \n"); } while (0 > 1);'), "S{C}")
        self.assertEqual(tokenizer('if (x > 0) for (j = 0; j < 10; j++) func(x, j);'), "I{S{C}}")
        self.assertEqual(tokenizer("; (x > y) ? func1(): func2();"), "I{C}I{C}")
        self.assertEqual(tokenizer("z = (x > y) ? func1(): func2();"), "I{AC}I{AC}")
        self.assertEqual(tokenizer("z = (x > y) ? x + y - 2: x - y + 2;"), "I{AMM}I{AMM}")
        self.assertEqual(tokenizer("z = (x > y) ? x + func(y): x - func(y) + 2;"), "I{AM}I{AMM}")
        self.assertEqual(tokenizer("z = (x > y) ? x : y;"), "I{A}I{A}")
        self.assertEqual(tokenizer("z=(x>y)?x:y;"), "I{A}I{A}")
        self.assertEqual(tokenizer(";int z = (x > y) ? x : y;"), "I{A}I{A}")
        self.assertEqual(tokenizer(" }  int z = (x > y) ? x : y;"), "}I{A}I{A}")
        self.assertEqual(tokenizer(" } z = (x > y) ? x : y;"), "}I{A}I{A}")
        self.assertEqual(tokenizer("; x == 10 ? func(x) : 64 + x;"), "I{C}I{M}")
        self.assertEqual(tokenizer("y = x == 10 ? func(x) : 64 + x;"), "I{AC}I{AM}")
        self.assertEqual(tokenizer(";return x == 10 ? func(x) : 64 + x;"), "I{RC}I{RM}")
        self.assertEqual(tokenizer(self.switch_str), "I{C}I{C}I{C}")
        switch_str = "int updateCriticalNumber(int value){switch (value){case 0:return value + 64;break;case -10:{" \
                     "return 10;break;}case 10:{return func(value);break;}}} "
        self.assertEqual(tokenizer(switch_str), "F{I{RM}I{R}I{RC}}")
        switch_str = "int updateCriticalNumber (int value)\n{ switch (value) {\ncase\n0: return value + 64; break; " \
                     "case -10: { return 10; break; } case 10: { return func(value); break; }}} "
        self.assertEqual(tokenizer(switch_str), "F{I{RM}I{R}I{RC}}")
        switch_str = "int updateCriticalNumber (int value)\n{ switch (value) {\ncase\n0: { return value + 64; break;}" \
                     "case -10:  return 10; break; default: { return func(value); break; }}} "
        self.assertEqual(tokenizer(switch_str), "F{I{RM}I{R}I{RC}}")
        switch_str = "int updateCriticalNumber (int value)\n{ switch (value) {\ncase\n0: { return value + 64; break;}" \
                     "case -10:  return 10; break; default:  return func(value); break; }} "
        self.assertEqual(tokenizer(switch_str), "F{I{RM}I{R}I{RC}}")
        switch_str = "int updateCriticalNumber (int value)\n{ switch (value) {\ncase\n0: { return value + 64; }" \
                     "case -10: if (x > 80) return 10; default:  return func(value);}} "
        self.assertEqual(tokenizer(switch_str), "F{I{RM}I{I{R}}I{RC}}")
        test_str = "if(*output==NULL)"\
                       "*output = (char**) malloc(count*sizeof(char*));"\
                   "else"\
                       "*output = (char**) realloc (*output,count*sizeof(char*));"
        self.assertEqual(tokenizer(test_str), "I{ATC}I{ATC}")
        self.assertEqual(tokenizer("while(*output == NULL) *output = (char**) malloc(count * sizeof(char*));"), "S{ATC}")
        self.assertEqual(tokenizer('#include <stdio.h>\n#define print(a) printf("%d \n", a);\nint main(void){\nint x = 10;\nprint(x);\nreturn 0;\n}'), "F{NACR}")

    def assert_tokens_list(self, current, true):
        self.assertEqual(len(current), len(true))
        for i in range(len(current)):
            self.assertEqual(current[i].symbol, true[i].symbol)
            self.assertEqual(current[i].start, true[i].start)
            self.assertEqual(current[i].end, true[i].end)

    def test_get_function_names(self):
        self.assertListEqual(CTokenizer.get_function_names("int sum(int a, int b) {"), ["sum"])
        self.assertListEqual(CTokenizer.get_function_names("void  _sum (){"), ["_sum"])
        self.assertListEqual(CTokenizer.get_function_names(" int **  _sum (int a[]){"), ["_sum"])
        src = "int (*select(void))(void){return 0;}"
        self.assertListEqual(CTokenizer.get_function_names(src), ["select"])
        self.assertListEqual(CTokenizer.get_function_names(src * 2), ["select"])
        src = src + "int (*test(void))(void){return 0;}"
        self.assertListEqual(sorted(CTokenizer.get_function_names(src)), ["select", "test"])
        src = "int operation1(int (*op)(int, int), int a, int b){"
        self.assertListEqual(CTokenizer.get_function_names(src), ["operation1"])
        self.assertListEqual(CTokenizer.get_function_names("int sum(int n, ...){"), ["sum"])
        src = "struct time addminutes(struct time t, int minutes){"
        self.assertListEqual(CTokenizer.get_function_names(src), ["addminutes"])
        src = "int sum(int a, int b) { return a + b; }"
        self.assertListEqual(CTokenizer.get_function_names(src), ["sum"])
        src = "int sum(int a, int b) { return a + b; } int mult(int a, int b) { return a * b; } "
        self.assertListEqual(sorted(CTokenizer.get_function_names(src)), ["mult", "sum"])
        self.assertListEqual(CTokenizer.get_function_names("while (x < 10) { x++; }"), [])
        self.assertListEqual(CTokenizer.get_function_names("do { x++; }while (x < 10);"), [])
        src = "for (i = 0; i < 10; i++) { func(i); }"
        self.assertListEqual(CTokenizer.get_function_names(src), [])

    def test_replace_tokens_in_src(self):
        tokens = [
            Token("T", 1, 20),
        ]
        self.assertEqual(CTokenizer.replace_tokens_in_src("if(x < 10) int a = 10", tokens), "i" + "." * 19 + "0")
        tokens = [
            Token("T", 1, 20),
        ]
        self.assertEqual(CTokenizer.replace_tokens_in_src("if(x < 10) int a = 10", tokens, is_full_replace=False), "i" + "." * 18 + "10")
        tokens = [
            Token("T", 1, 10),
            Token("T", 18, 20),
        ]
        self.assertEqual(CTokenizer.replace_tokens_in_src("if(x < 10) int a = 10", tokens), "i" + "." * 9 + " int a =" + ".." + "0")
        tokens = [
            Token("T", 0, 12),
            Token("T", 10, 21),
        ]
        self.assertEqual(CTokenizer.replace_tokens_in_src("if(x < 10) int a = 10", tokens), "." * 21)

    def test_get_tokens_missing_curly_braces(self):
        src = "if(x < 10) int a = 10;"
        tokens = [
            Token("{", 10, 10),
            Token("}", 21, 21),
        ]
        self.assert_tokens_list(CTokenizer.get_tokens_missing_curly_braces(src), tokens)

        src = " while(x < 10) int a = 10; "
        tokens = [
            Token("{", 14, 14),
            Token("}", 25, 25),
        ]
        self.assert_tokens_list(CTokenizer.get_tokens_missing_curly_braces(src), tokens)

        src = " while(6 < func(x)) int a = 10; "
        tokens = [
            Token("{", 17, 17),
            Token("}", 30, 30),
        ]
        self.assert_tokens_list(CTokenizer.get_tokens_missing_curly_braces(src), tokens)

        src = " while(x < 10) if(x % 2 == 0) a++;"
        tokens = [
            Token("{", 14, 14),
            Token("{", 29, 29),
            Token("}", 33, 33),
            Token("}", 33, 33),
        ]
        self.assert_tokens_list(sorted(CTokenizer.get_tokens_missing_curly_braces(src), key=attrgetter('start', 'end')), tokens)

        src = "while(x < 10) do a++; while(x % 2 == 0);"
        tokens = [
            Token("{", 13, 13),
            Token("{", 16, 16),
            Token("}", 20, 20),
            Token("}", 20, 20),
        ]
        self.assert_tokens_list(sorted(CTokenizer.get_tokens_missing_curly_braces(src), key=attrgetter('start', 'end')), tokens)

        src = "if (i > 0) for(;;;) i++;"
        tokens = [
            Token("{", 10, 10),
            Token("{", 19, 19),
            Token("}", 23, 23),
            Token("}", 23, 23),
        ]
        self.assert_tokens_list(sorted(CTokenizer.get_tokens_missing_curly_braces(src), key=attrgetter('start', 'end')), tokens)

        src = "if (i > 0) i++; else i--;"
        tokens = [
            Token("{", 10, 10),
            Token("}", 14, 14),
            Token("{", 20, 20),
            Token("}", 24, 24),
        ]
        self.assert_tokens_list(sorted(CTokenizer.get_tokens_missing_curly_braces(src), key=attrgetter('start', 'end')), tokens)

        src = "do if (i > 0) return func(); while(i > 10);"
        tokens = [
            Token("{", 2, 2),
            Token("{", 13, 13),
            Token("}", 27, 27),
            Token("}", 27, 27),
        ]
        self.assert_tokens_list(sorted(CTokenizer.get_tokens_missing_curly_braces(src), key=attrgetter('start', 'end')), tokens)

        src = " while((x > 8) && x < 19) if(y > 0) y--;else return y;"
        tokens = [
            Token("{", 14, 14),
            Token("{", 35, 35),
            Token("}", 39, 39),
            Token("{", 44, 44),
            Token("}", 53, 53),
            Token("}", 53, 53),
        ]
        self.assert_tokens_list(sorted(CTokenizer.get_tokens_missing_curly_braces(src), key=attrgetter('start', 'end')), tokens)

        src = " while((x > 8) && x < 19) if(y > 0) y--;else if (func()) return y;"
        tokens = [
            Token("{", 14, 14),
            Token("{", 35, 35),
            Token("}", 39, 39),
            Token("{", 44, 44),
            Token("{", 54, 54),
            Token("}", 65, 65),
            Token("}", 65, 65),
            Token("}", 65, 65),
        ]
        self.assert_tokens_list(sorted(CTokenizer.get_tokens_missing_curly_braces(src), key=attrgetter('start', 'end')), tokens)


if __name__ == '__main__':
    unittest.main()
