import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from io import StringIO
from unittest.mock import patch
from search import print_word, find_pages, compute_tfidf, parse_query

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
        self.assertEqual(result, [])
    
    # Test the find_pages function when the list of words is empty
    def test_find_pages_empty_list(self):
        result = find_pages([], self.index)
        self.assertEqual(result, [])

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
    
    def test_parse_query_and(self):
        # Add another word to the index for testing
        self.index["world"] = {
            "http://example.com": {
                "frequency": 1,
                "positions": [1]
            }
        }
        result = parse_query("hello AND world", self.index)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "http://example.com")

    def test_parse_query_or(self):
        result = parse_query("hello OR world", self.index)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "http://example.com")

    def test_parse_query_not(self):
        result = parse_query("hello NOT world", self.index)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "http://example.com")

    def test_parse_query_word_not_in_index_and(self):
        result = parse_query("hello AND world", self.index)
        self.assertEqual(result, [])
    
    def test_parse_query_word_not_in_index_or(self):
        result = parse_query("hello OR world", self.index)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "http://example.com")
     
    def test_parse_query_no_words_found_or(self):
        result = parse_query("foo OR bar", self.index)
        self.assertEqual(result, [])
    
    def test_parse_query_word_not_in_index_not(self):
        result = parse_query("hello NOT world", self.index)
        self.assertEqual(result[0][1], "http://example.com")
    
    def test_and_missing_second_term(self):
        result = parse_query("hello AND ", self.index)
        self.assertEqual(result, [])

    def test_and_missing_first_term(self):
        result = parse_query(" AND hello", self.index)
        self.assertEqual(result, [])

    def test_and_same_word_twice(self):
        result = parse_query("hello AND hello", self.index)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "http://example.com")

    def test_and_second_word_not_in_index(self):
        result = parse_query("hello AND zzz", self.index)
        self.assertEqual(result, [])

    def test_and_three_terms(self):
        self.index["world"] = {"http://example.com": {"frequency": 1, "positions": [1]}}
        self.index["foo"] = {"http://example.com": {"frequency": 1, "positions": [2]}}
        result = parse_query("hello AND world AND foo", self.index)
        self.assertEqual(len(result), 1)

    def test_and_extra_whitespace(self):
        self.index["world"] = {"http://example.com": {"frequency": 1, "positions": [1]}}
        result = parse_query("hello  AND  world", self.index)
        self.assertEqual(len(result), 1)

    def test_or_missing_second_term(self):
        result = parse_query("hello OR ", self.index)
        self.assertEqual(result, [])

    def test_or_missing_first_term(self):
        result = parse_query(" OR hello", self.index)
        self.assertEqual(result, [])

    def test_or_same_word_twice(self):
        result = parse_query("hello OR hello", self.index)
        self.assertEqual(len(result), 1)

    def test_or_neither_word_in_index(self):
        result = parse_query("zzz OR yyy", self.index)
        self.assertEqual(result, [])

    def test_or_only_one_word_in_index(self):
        result = parse_query("hello OR zzz", self.index)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "http://example.com")

    def test_or_three_terms(self):
        self.index["world"] = {"http://example.com/page2": {"frequency": 1, "positions": [1]}}
        result = parse_query("hello OR world OR zzz", self.index)
        self.assertEqual(len(result), 2)

    def test_or_extra_whitespace(self):
        result = parse_query("hello  OR  zzz", self.index)
        self.assertEqual(len(result), 1)

    def test_not_missing_second_term(self):
        result = parse_query("hello NOT ", self.index)
        self.assertEqual(result, [])

    def test_not_missing_first_term(self):
        result = parse_query(" NOT hello", self.index)
        self.assertEqual(result, [])

    def test_not_same_word(self):
        result = parse_query("hello NOT hello", self.index)
        self.assertEqual(result, [])

    def test_not_excluded_word_not_in_index(self):
        result = parse_query("hello NOT zzz", self.index)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "http://example.com")

    def test_not_three_terms(self):
        result = parse_query("hello NOT world NOT foo", self.index)
        self.assertEqual(result, [])

    def test_not_extra_whitespace(self):
        result = parse_query("hello  NOT  zzz", self.index)
        self.assertEqual(len(result), 1)

    def test_empty_query(self):
        result = parse_query("", self.index)
        self.assertEqual(result, [])

    def test_whitespace_only_query(self):
        result = parse_query("   ", self.index)
        self.assertEqual(result, [])

    def test_mixed_operators(self):
        result = parse_query("hello AND world OR foo", self.index)
        # AND takes priority, OR is treated as part of second term
        self.assertIsInstance(result, list)

    def test_suggest_word_match(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            print_word("hallo", self.index)  # Misspelled "hello"
            output = mock_stdout.getvalue()
            self.assertIn("Did you mean: hello?", output)
    
    def test_suggest_word_no_match(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            print_word("xyzaaabc", self.index)  # No similar word in index
            output = mock_stdout.getvalue()
            self.assertIn("No similar words found in index for 'xyzaaabc'.", output)


if __name__ == '__main__':
    unittest.main()