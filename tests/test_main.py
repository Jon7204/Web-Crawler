import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from unittest.mock import patch
from io import StringIO
from main import main

class TestMain(unittest.TestCase):
    
    # Test load with no index file
    def test_load_no_file(self):
        with patch('os.path.exists', return_value=False):
            with patch('builtins.input', side_effect=['load', 'quit']):
                with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                    main()
                    output = mock_stdout.getvalue()
                    self.assertIn("No index found. Please build the index first.", output)

    # Test load with a valid index file
    def test_load_with_file(self):
        index_data = '{"test": ["page1", "page2"]}'
        with patch('os.path.exists', return_value=True):
            with patch('builtins.open', unittest.mock.mock_open(read_data=index_data)):
                with patch('builtins.input', side_effect=['load', 'quit']):
                    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                        main()
                        output = mock_stdout.getvalue()
                        self.assertIn("Index loaded from data/index.json", output)

    # Test print command with no index loaded
    def test_print_no_index(self):
        with patch('builtins.input', side_effect=['print test', 'quit']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                self.assertIn("No index loaded. Please build or load the index first.", output)
    
    # Test find command with no index loaded
    def test_find_no_index(self):
        with patch('builtins.input', side_effect=['find test', 'quit']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                self.assertIn("No index loaded. Please build or load the index first.", output)

    # Test unknown command
    def test_unknown_command(self):
        with patch('builtins.input', side_effect=['unknown', 'quit']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                self.assertIn("Unknown command. Please try again.", output)
    
    # Test quit command with all three quitting variations
    def test_quit_command(self):
        with patch('builtins.input', side_effect=['quit']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                self.assertEqual(output, "")
        
        with patch('builtins.input', side_effect=['q']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                self.assertEqual(output, "")
        
        with patch('builtins.input', side_effect=['exit']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                self.assertEqual(output, "")
    
    # Test print command with a valid index
    def test_print_with_index(self):
        fake_index = '{"test": {"http://example.com": {"frequency": 1, "positions": [0]}}}'
        with patch('os.path.exists', return_value=True):
            with patch('builtins.open', unittest.mock.mock_open(read_data=fake_index)):
                with patch('builtins.input', side_effect=['load', 'print test', 'quit']):
                    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                        main()
                        output = mock_stdout.getvalue()
                        self.assertIn("Word: 'test'", output)
                        self.assertIn("  URL: http://example.com", output)
                        self.assertIn("    Frequency: 1", output)
                        self.assertIn("    Positions: [0]", output)
    
    # Test find command with a valid index
    def test_find_with_index(self):
        fake_index = '{"test": {"http://example.com": {"frequency": 1, "positions": [0]}}}'
        with patch('os.path.exists', return_value=True):
            with patch('builtins.open', unittest.mock.mock_open(read_data=fake_index)):
                with patch('builtins.input', side_effect=['load', 'find test', 'quit']):
                    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                        main()
                        output = mock_stdout.getvalue()
                        print(repr(output))
                        self.assertIn("Pages containing all words ['test']:", output)
                        self.assertIn("  http://example.com", output)

if __name__ == '__main__':
    unittest.main()