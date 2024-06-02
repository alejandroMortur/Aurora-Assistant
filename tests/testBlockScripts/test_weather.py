import pytest
from unittest.mock import patch, Mock
from src.virtual_assistant.PYFuncionModules.weatherModule import get_weather

# Test for the get_weather function
def test_get_weather():
    # Define a mock queue to capture messages from the function
    fake_queue = Mock()

    # Mock the call to the Weather API
    with patch('requests.get') as mock_get:
        # Configure the expected behavior of the mock
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "currentConditions": {
                "temp": 20,
                "humidity": 60,
                "windspeed": 10
            }
        }

        # Execute the function under test
        result = get_weather("New York", "api_key", "en-US", fake_queue)

        # Verify that the appropriate message was printed
        fake_queue.put.assert_called_once_with("Wheater information found correctly")

        # Verify that the function returns the expected phrase
        expected_phrase = "At this moment in New York, it is 20 degrees Celsius, with a humidity of 60% and a wind speed of 10 km/h."
        assert result == expected_phrase
