import unittest
from src.tokenizers.c_tokenizer import CTokenizer


class TestCTokenizer(unittest.TestCase):
    def setUp(self):
        self.tokenizer = CTokenizer()

    def test__clear_comments(self):
        self.assertEqual(self.tokenizer._clear_comments(""), "")
        self.assertEqual(self.tokenizer._clear_comments("//comment"), "")
        self.assertEqual(self.tokenizer._clear_comments("// comment"), "")
        self.assertEqual(self.tokenizer._clear_comments("//comment\n"), "")
        self.assertEqual(self.tokenizer._clear_comments("// comment\n"), "")
        self.assertEqual(self.tokenizer._clear_comments("//  comment //comment"), "")
        self.assertEqual(self.tokenizer._clear_comments("int x = 0; // integer x is 0"), "int x = 0; ")
        self.assertEqual(self.tokenizer._clear_comments("// integer x is 0\nint x = 0;"), "int x = 0;")
        self.assertEqual(self.tokenizer._clear_comments("//comment1\nint x = 0;\n// comment2"), "int x = 0;\n")
        self.assertEqual(self.tokenizer._clear_comments("/*comment*/"), "")
        self.assertEqual(self.tokenizer._clear_comments("/* comment */"), "")
        self.assertEqual(self.tokenizer._clear_comments(" /* comment */ "), "  ")
        self.assertEqual(self.tokenizer._clear_comments("/*int x = 0; float y = 1.0; */"), "")
        self.assertEqual(self.tokenizer._clear_comments("/*int x = 0;\nfloat y = 1.0;\n*/"), "")

    def test__clear_import(self):
        self.assertEqual(self.tokenizer._clear_import("#include <stdio.h>"), "")
        self.assertEqual(self.tokenizer._clear_import(' #include "max.h"  '), "")
        self.assertEqual(self.tokenizer._clear_import('#include <stdio.h>\n#include "max.h"'), "")
        self.assertEqual(self.tokenizer._clear_import('#include <stdio.h>\n#include "max.h"\n'), "")
        self.assertEqual(self.tokenizer._clear_import('#include <stdio.h>\n#include "max.h"\nint x = 0 ; \n'), "int x = 0 ; \n")

    def test_tokenize_base_case(self):
        self.assertEqual(self.tokenizer.tokenize("// comment"), "")
        self.assertEqual(self.tokenizer.tokenize("#include <stdio.h>"), "")
        self.assertEqual(self.tokenizer.tokenize("unsigned long testValue = 9999999;"), "NA")
        self.assertEqual(self.tokenizer.tokenize("unsigned char testValue;"), "B")
        self.assertEqual(self.tokenizer.tokenize("long double testValue;"), "D")
        self.assertEqual(self.tokenizer.tokenize("signed char **pointer;"), "P")
        self.assertEqual(self.tokenizer.tokenize("int *pointer = &value;"), "PA")
        self.assertEqual(self.tokenizer.tokenize("int value = *ptr;"), "NA")
        # self.assertEqual(self.tokenizer.tokenize("void* voidptr = pointer;"), "PA")
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
        self.assertEqual(self.tokenizer.tokenize("if(a > b) return a; else a++;"), "IRIM")
        self.assertEqual(self.tokenizer.tokenize("if(c > b) return c; else if(b < c) return b; else return 0;"), "IRIRIR")
        self.assertEqual(self.tokenizer.tokenize("if(func(a, b)) return a;"), "IR")
        # self.assertEqual(self.tokenizer.tokenize("z = (x > y) ? x: y;"), "IAIA")
        # self.assertEqual(self.tokenizer.tokenize("z = (x > y) ? func1(): func2();"), "IACIAC")
        # self.assertEqual(self.tokenizer.tokenize("(x > y) ? func1(): func2();"), "ICIC")
        self.assertEqual(self.tokenizer.tokenize("int value = T;"), "NA")
        self.assertEqual(self.tokenizer.tokenize("int value = T + A;"), "NAM")
        self.assertEqual(self.tokenizer.tokenize("void* value = func(T, A, X);"), "PAC")
        self.assertEqual(self.tokenizer.tokenize("while(x < 10) x += 1;"), "SAM")
        self.assertEqual(self.tokenizer.tokenize("for(int i = 0; i < 10; i++) compare(func(i), 0);"), "SC")
        self.assertEqual(self.tokenizer.tokenize("while(x < 10) if(x % 2 == 0) y += x;"), "SIAM")
        self.assertEqual(self.tokenizer.tokenize("while(x < 10) if(x % 2 == 0) y += x; else return 0;"), "SIAMIR")


if __name__ == '__main__':
    unittest.main()
