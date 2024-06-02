import pytest
import os
from unittest.mock import patch, Mock
from src.virtual_assistant.PYFuncionModules.programsHandlerModule import open_program, close_program

# Test for the open_program function
def test_open_program():
    # Define a mock queue to capture messages from the function
    fake_queue = Mock()

    # Mock the call to subprocess.Popen
    with patch('subprocess.Popen') as mock_popen:
        # Configure the expected behavior of the mock
        mock_popen.return_value = Mock()

        # Execute the function under test
        open_program("notepad", fake_queue)

        # Verify that the appropriate message was printed
        fake_queue.put.assert_called_once()

        # Verify that subprocess.Popen was called with the correct program
        mock_popen.assert_called_once_with([os.path.join(os.environ['SystemRoot'], 'System32', 'notepad.exe')])

# Test for the close_program function
def test_close_program():
    # Define a mock queue to capture messages from the function
    fake_queue = Mock()

    # Mock the call to subprocess.run
    with patch('src.virtual_assistant.PYFuncionModules.programsHandlerModule.subprocess.run') as mock_run:
        # Execute the function under test
        close_program("notepad", fake_queue)

        # Verify that the appropriate message was printed
        fake_queue.put.assert_called_once()

        # Verify that subprocess.run was not called
        mock_run.assert_not_called()
