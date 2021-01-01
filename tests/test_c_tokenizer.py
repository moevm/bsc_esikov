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
        self.assertEqual(self.tokenizer._clear_import('#include "max.h"  '), "")
        self.assertEqual(self.tokenizer._clear_import('#include <stdio.h>\n#include "max.h"'), "")
        self.assertEqual(self.tokenizer._clear_import('#include <stdio.h>\n#include "max.h"\n'), "")
        self.assertEqual(self.tokenizer._clear_import('#include <stdio.h>\n#include "max.h"\nint x = 0 ; \n'), "int x = 0 ; \n")


if __name__ == '__main__':
    unittest.main()
