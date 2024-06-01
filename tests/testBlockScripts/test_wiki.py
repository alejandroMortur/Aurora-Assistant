import pytest
from unittest.mock import patch, Mock
from src.virtual_assistant.PYFuncionModules.wikiModule import search_wikipedia_summary

# Test for the search_wikipedia_summary function
def test_search_wikipedia_summary():
    # Define a mock queue to capture messages from the function
    fake_queue = Mock()

    # Mock the call to the Wikipedia API
    with patch('wikipedia.summary') as mock_summary:
        # Configure the expected behavior of the mock
        mock_summary.return_value = "Summary of the Wikipedia page"

        # Execute the function under test
        result = search_wikipedia_summary("Python programming language", "en", fake_queue, 2)

        # Verify that no message was printed to the queue
        fake_queue.put.assert_not_called()

        # Verify that the function returns the correct summary
        expected_summary = "Summary of the Wikipedia page"
        assert result == expected_summary
