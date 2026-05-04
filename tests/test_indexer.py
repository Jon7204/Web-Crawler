import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from indexer import build_index, extract_text, tokenize

class TestIndexer(unittest.TestCase):

    # Test the build_index function with various inputs
    def test_build_index(self):
        pages = {
            "http://example.com": "<html><body><p>Hello world</p></body></html>",
            "http://example.com/page1": "<html><body><p>Hello again</p></body></html>"
        }
        index = build_index(pages)
        self.assertIn("hello", index)
        self.assertIn("world", index)
        self.assertIn("again", index)
        self.assertIn("http://example.com", index["hello"])
        self.assertIn("http://example.com/page1", index["hello"])
        self.assertEqual(index["hello"]["http://example.com"]["frequency"], 1)
        self.assertEqual(index["hello"]["http://example.com/page1"]["frequency"], 1)
    
    # Test the extract_text function exclusively with a simple HTML input
    def test_extract_text(self):
        html = "<html><body><p>Hello world</p></body></html>"
        text = extract_text(html)
        self.assertEqual(text, "Hello world")

    # Test the tokenize function exclusively with a simple input string
    def test_tokenize(self):
        text = "Hello world! This is a test."
        tokens = tokenize(text)
        self.assertEqual(tokens, ["hello", "world", "test"])
    
    # Test the build_index function with an empty page
    def test_empty_page(self):
        pages = {
            "http://example.com": "<html><body></body></html>"
        }
        index = build_index(pages)
        self.assertEqual(index, {})
    
    # Test the build_index function with a page that has multiple occurrences of the same word
    def test_multiple_occurrences(self):
        pages = {
            "http://example.com": "<html><body><p>Hello world. Hello again.</p></body></html>"
        }
        index = build_index(pages)
        self.assertIn("hello", index)
        self.assertEqual(index["hello"]["http://example.com"]["frequency"], 2)
        self.assertEqual(index["hello"]["http://example.com"]["positions"], [0, 2])

if __name__ == '__main__':
    unittest.main()