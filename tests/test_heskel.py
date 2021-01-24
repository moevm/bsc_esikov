import unittest
from src.algorithms.heskel import Heskel


class TestHeskel(unittest.TestCase):
    def test_split_into_n_gramms(self):
        self.assertSetEqual(Heskel.split_into_n_gramms("ABCDEF", -1), set())
        self.assertSetEqual(Heskel.split_into_n_gramms("ABCDEF", 0), set())
        self.assertSetEqual(Heskel.split_into_n_gramms("ABCDEF", 1), {"A", "B", "C", "D", "E", "F"})
        self.assertSetEqual(Heskel.split_into_n_gramms("ABCDEF", 2), {"AB", "BC", "CD", "DE", "EF"})
        self.assertSetEqual(Heskel.split_into_n_gramms("ABCDEF", 3), {"ABC", "BCD", "CDE", "DEF"})
        self.assertSetEqual(Heskel.split_into_n_gramms("ABCDEF", 4), {"ABCD", "BCDE", "CDEF"})
        self.assertSetEqual(Heskel.split_into_n_gramms("ABCDEF", 5), {"ABCDE", "BCDEF"})
        self.assertSetEqual(Heskel.split_into_n_gramms("ABCDEF", 6), {"ABCDEF"})
        self.assertSetEqual(Heskel.split_into_n_gramms("ABCDEF", 7), set())

    def test_search(self):
        heskel = Heskel("ABCDEFGHIJ", length_n_gramm=2)
        self.assertEqual(heskel.search("ABCDEFGHIJ"), 100)
        self.assertEqual(heskel.search("KLMNOPQRST"), 0)
        self.assertEqual(heskel.search("ABCDEFGHIZ"), round((8 / 10) * 100))
        self.assertEqual(heskel.search("ABCDEFGHZZ"), round((7 / 11) * 100))
        self.assertEqual(heskel.search("ABCDEZZZZZ"), round((4 / 11) * 100))
        self.assertEqual(heskel.search("ABCDEVWXYZ"), round((4 / 14) * 100))
        heskel = Heskel("S{AM}R", length_n_gramm=2)
        self.assertEqual(heskel.search("S{AM}A"), round((4 / 6) * 100))
        heskel = Heskel("S{AM}R", length_n_gramm=4)
        self.assertEqual(heskel.search("S{AM}A"), round((2 / 4) * 100))
        heskel = Heskel("S{I{AM}}A", length_n_gramm=2)
        self.assertEqual(heskel.search("S{I{AR}}R"), round((5 / 11) * 100))


if __name__ == '__main__':
    unittest.main()
