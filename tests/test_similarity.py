import unittest
from src.similarity import Similarity
from src.src_file import SrcFile
from src.tokenizers.c_tokenizer import CTokenizer


class TestSimilarity(unittest.TestCase):
    def setUp(self):
        self.file_1 = SrcFile("file1", "file1", "int x = 0; return x;")
        self.file_2 = SrcFile("file2", "file2", "double x = func(a, b); return;")
        self.tokenizer = CTokenizer()
        self.file_1.tokens = self.tokenizer.tokenize(self.file_1.src)
        self.file_2.tokens = self.tokenizer.tokenize(self.file_2.src)
        self.similarity = Similarity(self.file_1, self.file_2, ["A", "R"])

    def test_get_str_src_from_token_str(self):
        self.assertEqual(self.similarity._get_str_src_from_token_str(self.file_1, "R"), "return ")
        self.assertEqual(self.similarity._get_str_src_from_token_str(self.file_2, "R"), "return;")

    def test_get_similarity_src(self):
        file_1_sim_str_list, file_2_sim_str_list = self.similarity.get_similarity_src()
        self.assertListEqual(sorted(file_1_sim_str_list), ["= 0;", "return "])
        self.assertListEqual(sorted(file_2_sim_str_list), ["= func(a, b);", "return;"])


if __name__ == '__main__':
    unittest.main()
