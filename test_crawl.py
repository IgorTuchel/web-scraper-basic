import unittest
from crawl import normalize_url,get_urls_from_html


class TestCrawl(unittest.TestCase):
    def test_normalize_url1(self):
        urls = {
            "https://blog.boot.dev/path": "blog.boot.dev/path"
                }
        for url in urls:
            actual = normalize_url(url)
            self.assertEqual(actual, urls[url])

    def test_normalize_url2(self):
        input_url = "http://google.com"
        actual = normalize_url(input_url)
        expected = "google.com"
        self.assertEqual(actual, expected)

    def test_normalize_url3(self):
        input_url = "www.blog.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url4(self):
        input_url = "https://www.blog.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute1(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="https://blog.boot.dev"><span>Boot.dev></span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute2(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="https://blog.boot.dev/xd"><span>Boot.dev></span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/xd"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute3(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="https://google.com"><span>Boot.dev></span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://google.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative1(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="/boots"><span>Boot.dev></span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/boots"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative2(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="https://google.com/boots"><span>Boot.dev></span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://google.com/boots"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative3(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="/who/is/boots"><span>Boot.dev></span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/who/is/boots"]
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()