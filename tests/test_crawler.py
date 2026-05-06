import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import requests
import unittest
from unittest.mock import patch, MagicMock
from crawler import crawl

class TestCrawler(unittest.TestCase):

    # Test that the crawler returns the content of the page
    def test_returns_page_content(self):
       mock_response = MagicMock()
       mock_response.text = "<html><body><p>Hello</p></body></html>"
       mock_response.raise_for_status = MagicMock()
       with patch('crawler.requests.get', return_value=mock_response):
           pages = crawl("http://example.com", politeness_window=1)
           self.assertIn("http://example.com", pages)
           self.assertEqual(pages["http://example.com"], "<html><body><p>Hello</p></body></html>")

    # Test that the crawler follows links found on the page
    def test_follows_links(self):
        def fake_get(url, **kwargs):
            mock_response = MagicMock()
            mock_response.raise_for_status = MagicMock()
            if url == "http://example.com":
                mock_response.text = "<html><body><a href='http://example.com/page1'>Page 1</a></body></html>"
            else:
                mock_response.text = "<html><body><p>Page 1 Content</p></body></html>"
            return mock_response

        with patch('crawler.requests.get', side_effect=fake_get):
            pages = crawl("http://example.com", politeness_window=1)
            self.assertIn("http://example.com", pages)
            self.assertIn("http://example.com/page1", pages)
            self.assertEqual(pages["http://example.com/page1"], "<html><body><p>Page 1 Content</p></body></html>")

    # Test that the crawler does not follow links that have already been visited
    def test_does_not_follow_visited_links(self):
        def fake_get(url, **kwargs):
            mock_response = MagicMock()
            mock_response.raise_for_status = MagicMock()
            if url == "http://example.com":
                mock_response.text = "<html><body><a href='http://example.com'>Home</a></body></html>"
            else:
                mock_response.text = "<html><body><p>Home Content</p></body></html>"
            return mock_response

        with patch('crawler.requests.get', side_effect=fake_get):
            pages = crawl("http://example.com", politeness_window=1)
            self.assertIn("http://example.com", pages)
            self.assertEqual(len(pages), 1)  # Should only crawl the base URL once

    # Test that the crawler does not follow external links    
    def test_does_not_follow_external_links(self):
        def fake_get(url, **kwargs):
            mock_response = MagicMock()
            mock_response.raise_for_status = MagicMock()
            if url == "http://example.com":
                mock_response.text = "<html><body><a href='http://external.com'>External</a></body></html>"
            else:
                mock_response.text = "<html><body><p>External Content</p></body></html>"
            return mock_response

        with patch('crawler.requests.get', side_effect=fake_get):
            pages = crawl("http://example.com", politeness_window=1)
            self.assertIn("http://example.com", pages)
            self.assertNotIn("http://external.com", pages)  

    # Test that the crawler respects the politeness window between requests
    def test_respects_politeness_window(self):
        with patch('crawler.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.text = "<html><body><a href='http://example.com/page1'>Page 1</a></body></html>"
            mock_response.raise_for_status = MagicMock()
            mock_get.return_value = mock_response

            with patch('crawler.time.sleep') as mock_sleep:
                crawl("http://example.com", politeness_window=5)
                mock_sleep.assert_called_with(5)
    
    # Test that the crawler handles request exceptions gracefully
    def test_handles_request_exception(self):
        with patch('crawler.requests.get', side_effect=requests.RequestException("Network error")):
            with patch('crawler.print') as mock_print:
                pages = crawl("http://example.com", politeness_window=1)
                self.assertEqual(pages, {})
                mock_print.assert_called_with("  Failed to crawl http://example.com: Network error")

if __name__ == '__main__':
    unittest.main()