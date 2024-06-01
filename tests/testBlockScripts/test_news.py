import pytest
import os
from unittest.mock import patch, Mock
from datetime import datetime, timedelta
from dotenv import load_dotenv
from src.virtual_assistant.PYFuncionModules.newsModule import get_news_today

# Simulate the news API credentials
load_dotenv()
API_KEY = os.getenv('APINEWS')
QUERY = "bitcoin"
LANGUAGE = "en"
PAGE_SIZE = 10

# Test for the get_news_today function
def test_get_news_today():
    # Define a mock queue to capture messages from the function
    fake_queue = Mock()

    # Mock the call to the news API
    with patch('requests.get') as mock_get:
        # Configure the expected behavior of the mock
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "status": "ok",
            "totalResults": 0,  # Simulate no news headlines found
            "articles": []
        }

        # Execute the function under test
        news_list = get_news_today(API_KEY, QUERY, LANGUAGE, PAGE_SIZE, fake_queue)

        # Verify that the call to the API was made with the correct parameters
        mock_get.assert_called_once_with(
            f"https://newsapi.org/v2/everything?q={QUERY}&"
            f"from={datetime.today() - timedelta(days=7):%Y-%m-%d}&"
            f"to={datetime.today():%Y-%m-%d}&"
            f"sortBy=popularity&pageSize={PAGE_SIZE}&"
            f"language={LANGUAGE}&apiKey={API_KEY}"
        )

        # Verify that no news headlines were retrieved
        assert len(news_list) == 0

        # Verify that the appropriate message was sent to the mock queue
        fake_queue.put.assert_called_once_with("No headlines found.")
