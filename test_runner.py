import unittest
import tests.test_c_tokenizer as test_c_tokenizer
import tests.test_tokenizer as test_tokenizer
import tests.test_heskel as test_heskel
import tests.test_greedy_string_tiling as test_greedy_string_tiling
import tests.test_token as test_token
import tests.test_similarity as test_similarity
import tests.test_url_parser as test_url_parser


if __name__ == '__main__':
    testLoad = unittest.TestLoader()
    suites_list = [
        testLoad.loadTestsFromModule(test_c_tokenizer),
        testLoad.loadTestsFromModule(test_tokenizer),
        testLoad.loadTestsFromModule(test_heskel),
        testLoad.loadTestsFromModule(test_greedy_string_tiling),
        testLoad.loadTestsFromModule(test_token),
        testLoad.loadTestsFromModule(test_similarity),
        testLoad.loadTestsFromModule(test_url_parser),
    ]
    suites = unittest.TestSuite(suites_list)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suites)
