import unittest
from src.tokenizers.tokenizer import Tokenizer


class TestTokenizer(unittest.TestCase):
    def test_clear_space(self):
        self.assertEqual(Tokenizer.clear_space(" "), "")
        self.assertEqual(Tokenizer.clear_space("int x =   0; "), "intx=0;")
        self.assertEqual(Tokenizer.clear_space("\tint x = 0;\n"), "intx=0;")


if __name__ == '__main__':
    unittest.main()
