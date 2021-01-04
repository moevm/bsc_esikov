import unittest
import tests.test_c_tokenizer as test_c_tokenizer
import tests.test_tokenizer as test_tokenizer


if __name__ == '__main__':
    testLoad = unittest.TestLoader()
    suites_list = [
        testLoad.loadTestsFromModule(test_c_tokenizer),
        testLoad.loadTestsFromModule(test_tokenizer),
    ]
    suites = unittest.TestSuite(suites_list)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suites)
