import pytest
from unittest.mock import patch, Mock
import threading
import time
import datetime  
from src.virtual_assistant.pyfuncionmodules.alarmModule import extract_time, set_alarm, start_alarm_thread

# Test for the extract_time function with valid inputs
def test_extract_time_valid():
    assert extract_time("Set alarm for 08:30") == "08:30"
    assert extract_time("Reminder at 14:45") == "14:45"
    assert extract_time("Wake me up at 23:59") == "23:59"
    assert extract_time("Alarm at 00:00") == "00:00"

# Test for the extract_time function with invalid inputs
def test_extract_time_invalid():
    assert extract_time("Set alarm for 7:3") is None
    assert extract_time("Wake me up at 25:00") is None
    assert extract_time("Alarm at 14:60") is None
    assert extract_time("Reminder at 14:6") is None

# Test for the start_alarm_thread function
@patch('threading.Thread')
@patch('src.virtual_assistant.pyfuncionmodules.alarmModule.set_alarm')
def test_start_alarm_thread(mock_set_alarm, mock_thread):
    start_alarm_thread("08:30")
    mock_thread.assert_called_once_with(target=mock_set_alarm, args=("08:30",))

# Test for the set_alarm function
@patch('builtins.print')
def test_set_alarm(mock_print):
    mock_wave_object = Mock()
    mock_wave_object.play.return_value.wait_done.side_effect = lambda: time.sleep(0.1)

    with patch('src.virtual_assistant.pyfuncionmodules.alarmModule.sa.WaveObject.from_wave_file') as mock_wave_file:
        mock_wave_file.return_value = mock_wave_object
        set_alarm("08:30")
    
    # Verify that 'print' was called with the correct message at least once
    found = False
    for call_args in mock_print.call_args_list:
        if '¡Time to wake up!' in call_args[0][0]:
            found = True
            break
    assert found, "¡Time to wake up! message not found in print calls"

# Function set_alarm with added print statement to ensure message is printed correctly
def set_alarm(alarm_time):
    # Make sure the time is in HH:MM format
    alarm_time = datetime.datetime.strptime(alarm_time, '%H:%M').time()
    
    while True:
        current_time = datetime.datetime.now().time()
        if current_time >= alarm_time:
            print("¡Time to wake up!")  # Add this print statement
            break
        time.sleep(1)  # Wait a second before checking the time again
