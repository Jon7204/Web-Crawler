import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from indexer import build_index, extract_text, tokenize

class TestIndexer(unittest.TestCase):

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
    
    def test_extract_text(self):
        html = "<html><body><p>Hello world</p></body></html>"
        text = extract_text(html)
        self.assertEqual(text, "Hello world")

    def test_tokenize(self):
        text = "Hello world! This is a test."
        tokens = tokenize(text)
        self.assertEqual(tokens, ["hello", "world", "this", "is", "a", "test"])
    
    def test_empty_page(self):
        pages = {
            "http://example.com": "<html><body></body></html>"
        }
        index = build_index(pages)
        self.assertEqual(index, {})
    
    def test_multiple_occurrences(self):
        pages = {
            "http://example.com": "<html><body><p>Hello world. Hello again.</p></body></html>"
        }
        index = build_index(pages)
        self.assertIn("hello", index)
        self.assertEqual(index["hello"]["http://example.com"]["frequency"], 2)
        self.assertEqual(index["hello"]["http://example.com"]["positions"], [0, 2])