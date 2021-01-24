import unittest
from src.token import Token


class TestToken(unittest.TestCase):
    def setUp(self):
        self.token_list_1 = [
            Token("I", 0, 1),
            Token("M", 3, 10),
            Token("I", 12, 15),
            Token("R", 17, 20)
        ]
        self.token_list_2 = [
            Token("I", 0, 1),
            Token("{", 0.5, 0.5),
            Token("M", 3, 10),
            Token("}", 10.5, 10.5),
            Token("I", 12, 15),
            Token("{", 12.5, 12.5),
            Token("R", 17, 20),
            Token("}", 20.5, 20.5)
        ]
        self.token_list_3 = [
            Token("S", 0, 1),
            Token("I", 3, 10),
            Token("M", 12, 15)
        ]

    def test_get_tokens_str_from_token_list(self):
        self.assertEqual(Token.get_tokens_str_from_token_list(self.token_list_1), "IMIR")
        self.assertEqual(Token.get_tokens_str_from_token_list(self.token_list_2), "I{M}I{R}")
        self.assertEqual(Token.get_tokens_str_from_token_list(self.token_list_3), "SIM")

    def test_find_border_tokens_str_in_token_list(self):
        self.assertEqual(Token.find_border_tokens_str_in_token_list(self.token_list_1, "IMI"), (0, 15))
        self.assertEqual(Token.find_border_tokens_str_in_token_list(self.token_list_1, "IMIR"), (0, 20))
        self.assertEqual(Token.find_border_tokens_str_in_token_list(self.token_list_1, "MIR"), (3, 20))
        self.assertIsNone(Token.find_border_tokens_str_in_token_list(self.token_list_1, "S{M}"))
        self.assertEqual(Token.find_border_tokens_str_in_token_list(self.token_list_2, "I{M}"), (0, 10.5))
        self.assertEqual(Token.find_border_tokens_str_in_token_list(self.token_list_2, "M}I{R}"), (3, 20.5))
        self.assertEqual(Token.find_border_tokens_str_in_token_list(self.token_list_3, "SIM"), (0, 15))
        self.assertIsNone(Token.find_border_tokens_str_in_token_list(self.token_list_3, "SIMM"))
        self.assertIsNone(Token.find_border_tokens_str_in_token_list(self.token_list_3, "NSIMM"))


if __name__ == '__main__':
    unittest.main()
