import json
import unittest
from rss_reader import RSSReader, parse_cli_arguments, InvalidSourceURL, NotRSSSource
from unittest.mock import MagicMock, patch
from bs4 import BeautifulSoup


class TestCase1(unittest.TestCase):

    cli_arguments = MagicMock(parse_cli_arguments().parse_args())
    cli_arguments.source = "http://*"
    cli_arguments.limit = None
    cli_arguments.date = None

    file = open("test_data_rss.xml", "r")
    test_data = file.read()
    file.close()

    response = MagicMock(content=test_data)
    response_empty = MagicMock(content="")
    RSSReader.cache_news = MagicMock()

    @patch('rss_reader.RSSReader.get_data_from_source')
    def test_validating_url(self, mock_get_data_from_source):
        invalid_url = ['', 'http://', 'https//', 'https:', 'http:', 'http://', 'https://', 'www.source.com']
        valid_url = ['http://domain', 'https://domain']
        mock_get_data_from_source.return_value = self.response
        reader = RSSReader(self.cli_arguments)
        for url in valid_url:
            reader._arg_url = url
            self.assertTrue(reader.validating_url(), f"URL '{url}' is passed")
        for url in invalid_url:
            reader._arg_url = url
            with self.assertRaises(InvalidSourceURL):
                reader.validating_url()

    @patch('rss_reader.request')
    def test_get_data_from_source(self, mock_request):
        mock_request.return_value = self.response
        reader = RSSReader(self.cli_arguments)
        self.assertEqual(reader.response.content, self.test_data)

    @patch('rss_reader.request')
    def test_get_tag_content(self, mock_request):
        mock_request.return_value = self.response
        bs = BeautifulSoup(self.response.content, "xml")
        reader = RSSReader(self.cli_arguments)
        self.assertEqual(reader.get_tag_content(bs.find("channel"), "title"), "TEST TITLE")
        self.assertEqual(reader.get_tag_content(bs.find("channel"), "no_tag"), None)

    @patch('rss_reader.request')
    def test_parse_response(self, mock_request):
        mock_request.return_value = self.response
        file = open("test_data_rss_result.txt", "r")
        test_data_result_rss = json.loads(file.read())
        file.close()
        reader = RSSReader(self.cli_arguments)
        news = reader.parse_response()
        self.assertEqual(news, test_data_result_rss)
        reader.response = self.response_empty
        with self.assertRaises(NotRSSSource):
            reader.parse_response()


if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)
