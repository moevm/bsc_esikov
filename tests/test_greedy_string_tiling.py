import unittest
from src.algorithms.greedy_string_tiling import GreedyStringTiling


class TestGreedyStringTiling(unittest.TestCase):
    def test_is_marked_match(self):
        self.assertFalse(GreedyStringTiling.is_marked_match({}, 0, 5))
        self.assertTrue(GreedyStringTiling.is_marked_match({0: True}, 0, 5))
        self.assertTrue(GreedyStringTiling.is_marked_match({4: "True"}, 0, 5))
        self.assertFalse(GreedyStringTiling.is_marked_match({7: "True"}, 0, 5))
        self.assertFalse(GreedyStringTiling.is_marked_match({2: 10}, 3, 8))

    def test_search(self):
        greedy = GreedyStringTiling("ABCDE")
        self.assertListEqual(greedy.search("ABCDEFGH"), ["ABCDE"])
        self.assertListEqual(greedy.search("ABCDE"), ["ABCDE"])
        self.assertListEqual(greedy.search("XYZBCD"), ["BCD"])
        self.assertListEqual(sorted(greedy.search("XYABCZWCDERR")), ["ABC", "DE"])
        self.assertListEqual(sorted(greedy.search("XYABZWCDERR")), ["AB", "CDE"])
        self.assertListEqual(sorted(greedy.search("XYABZWCDRERR")), ["AB", "CD"])
        self.assertListEqual(greedy.search("ABCABC"), ["ABC"])
        greedy = GreedyStringTiling("I{AMAM}")
        self.assertListEqual(greedy.search("I{AMAM}"), ["I{AMAM}"])
        self.assertListEqual(sorted(greedy.search("I{AMR}AM")), ["AM", "I{AM"])


if __name__ == '__main__':
    unittest.main()
