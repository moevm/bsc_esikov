import unittest
from src.network.url_parser import UrlParser


class TestUrlParser(unittest.TestCase):
    def test_parse_github_repo(self):
        owner, repo = UrlParser.parse_github_repo('https://github.com/microsoft/TypeScript')
        self.assertEqual(owner, 'microsoft')
        self.assertEqual(repo, 'TypeScript')

        self.assertRaises(ValueError, UrlParser.parse_github_repo, 'https://github.com/microsoft/TypeScript/blob/master/.gitattributes')

        self.assertRaises(ValueError, UrlParser.parse_github_repo, 'https://www.google.com/')

    def test_parse_github_file_path(self):
        url = 'https://github.com/microsoft/TypeScript/blob/master/.gitattributes'
        owner, repo, branch, path = UrlParser.parse_github_content_path(url)
        self.assertEqual(owner, 'microsoft')
        self.assertEqual(repo, 'TypeScript')
        self.assertEqual(branch, 'master')
        self.assertEqual(path, '.gitattributes')

        url = 'https://github.com/microsoft/TypeScript/blob/master/src/webServer/webServer.ts'
        owner, repo, branch, path = UrlParser.parse_github_content_path(url)
        self.assertEqual(owner, 'microsoft')
        self.assertEqual(repo, 'TypeScript')
        self.assertEqual(branch, 'master')
        self.assertEqual(path, 'src/webServer/webServer.ts')

        url = 'https://github.com/microsoft/TypeScript/blob/configBuild/scripts/authors.ts'
        owner, repo, branch, path = UrlParser.parse_github_content_path(url)
        self.assertEqual(owner, 'microsoft')
        self.assertEqual(repo, 'TypeScript')
        self.assertEqual(branch, 'configBuild')
        self.assertEqual(path, 'scripts/authors.ts')

        url = 'https://github.com/microsoft/TypeScript/tree/master/doc'
        owner, repo, branch, path = UrlParser.parse_github_content_path(url)
        self.assertEqual(owner, 'microsoft')
        self.assertEqual(repo, 'TypeScript')
        self.assertEqual(branch, 'master')
        self.assertEqual(path, 'doc')

        self.assertRaises(ValueError, UrlParser.parse_github_content_path, 'https://www.google.com/')

    def test_is_url(self):
        self.assertTrue(UrlParser.is_url('https://github.com'))
        self.assertTrue(UrlParser.is_url('https://github.com/'))
        self.assertFalse(UrlParser.is_url('./dir/file.ext'))

    def test_is_github_repo_url(self):
        self.assertTrue(UrlParser.is_github_repo_url('https://github.com/microsoft/TypeScript'))
        self.assertFalse(UrlParser.is_github_repo_url('https://github.com/microsoft/TypeScript/blob/master/.gitattributes'))
        self.assertFalse(UrlParser.is_github_repo_url('https://www.google.com/'))


if __name__ == '__main__':
    unittest.main()
