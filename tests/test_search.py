import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from io import StringIO
from unittest.mock import patch
from search import print_word, find_pages, compute_tfidf

class TestSearchFunctions(unittest.TestCase):

    # Set up a sample index for testing
    def setUp(self):
        self.index = {
            "hello": {
                "http://example.com": {
                    "frequency": 2,
                    "positions": [0, 3]
                }
            }
        }

    # Test the print_word function
    def test_print_word(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            print_word("hello", self.index)
            output = mock_stdout.getvalue()
            self.assertIn("Word: 'hello'", output)
            self.assertIn("  URL: http://example.com", output)
            self.assertIn("    Frequency: 2", output)
            self.assertIn("    Positions: [0, 3]", output)

    # Test the find_pages function
    def test_find_pages(self):
        result = find_pages(["hello"], self.index)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "http://example.com")
        self.assertIsInstance(result[0][0], float)

    # Test the print_word function when the word is not in the index
    def test_print_word_word_not_in_index(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            print_word("world", self.index)
            output = mock_stdout.getvalue()
            self.assertIn("Word 'world' not found in index.", output)

    # Test the find_pages function when the word is not in the index
    def test_find_pages_word_not_in_index(self):
        result = find_pages(["world"], self.index)
        self.assertEqual(result, set())
    
    # Test the find_pages function when the list of words is empty
    def test_find_pages_empty_list(self):
        result = find_pages([], self.index)
        self.assertEqual(result, set())

    # Test the find_pages function with multiple words
    def test_find_pages_multiple_words(self):
        # Add another word to the index for testing
        self.index["world"] = {
            "http://example.com": {
                "frequency": 1,
                "positions": [1]
            }
        }
        result = find_pages(["hello"], self.index)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "http://example.com")
        self.assertIsInstance(result[0][0], float)
    
    # Test the compute_tfidf function
    def test_tfidf_computation(self):
        # Add another word to the index for testing
        self.index["world"] = {
            "http://example.com": {
                "frequency": 1,
                "positions": [1]
            }
        }
        tfidf_hello = compute_tfidf("hello", "http://example.com", self.index)
        tfidf_world = compute_tfidf("world", "http://example.com", self.index)
        self.assertAlmostEqual(tfidf_hello, -1.3862943611198906)
        self.assertAlmostEqual(tfidf_world, -0.6931471805599453)

if __name__ == '__main__':
    unittest.main()