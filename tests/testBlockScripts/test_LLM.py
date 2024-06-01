import pytest
from unittest.mock import patch, Mock
from src.virtual_assistant.LLMModule import getLLMText

# Test for the getLLMText function
def test_getLLMText():
    # Define a mock queue to capture messages from the function
    fake_queue = Mock()

    # Mock the call to OpenAI
    with patch('src.virtual_assistant.LLMModule.OpenAI') as mock_openai:
        # Configure the expected behavior of the mock
        mock_client = Mock()
        mock_completions = Mock()
        mock_completion = Mock()
        mock_choice = Mock()
        mock_message = Mock()
        mock_message.content = "This is a test response."
        mock_choice.message = mock_message
        mock_completion.choices = [mock_choice]
        mock_completions.create.return_value = mock_completion
        mock_client.chat.completions = mock_completions
        mock_openai.return_value = mock_client

        # Execute the function under test
        response = getLLMText("Test input", 50, "en-US", fake_queue)

        # Verify that the call to OpenAI was made with the correct parameters
        mock_openai.assert_called_once_with(base_url="http://localhost:1234/v1", api_key="lm-studio")

        # Verify that the correct message was printed
        fake_queue.put.assert_called_once_with("LLM respond corretly get")

        # Verify that the response is as expected
        assert response == "This is a test response."
