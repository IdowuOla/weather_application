import unittest
from weather_app import get_weather_description
from unittest.mock import patch, Mock
from weather_app import get_weather
from contextlib import redirect_stdout
from io import StringIO
import requests

class TestWeatherDescription(unittest.TestCase):

    def test_clear_sky(self):
         result = get_weather_description(0)
         self.assertEqual(result, "Clear sky")
        
    def test_partly_cloudy(self):
         result = get_weather_description(2)
         self.assertEqual(result, "Partly cloudy")
        
    def test_fog(self):
         result = get_weather_description(45)
         self.assertEqual(result, "Fog")
    
    def test_thunderstorm(self):
         result = get_weather_description(95)
         self.assertEqual(result, "Thunderstorm")

    def test_unknown_weather(self):
         result = get_weather_description(100)
         self.assertEqual(result, "Unknown weather condition")


class TestCitySearch(unittest.TestCase):

     @patch("weather_app.requests.get")
     def test_city_not_found(self, mock_get):
          mock_response = Mock()
          mock_response.json.return_value = {
               "results": []
          }
          mock_get.return_value = mock_response

          output = StringIO()
          with redirect_stdout(output):
               get_weather("Atlantis")
          
          self.assertIn("No result found",output.getvalue())
          self.assertEqual(mock_get.call_count, 1)




class TestAPIErrors(unittest.TestCase):
     @patch("weather_app.requests.get")
     def test_connection_error(self, mock_get):
          mock_get.side_effect = requests.exceptions.ConnectionError

          output = StringIO()
          with redirect_stdout(output):
               get_weather("London")
          
          self.assertIn("Unable to connect to the server", output.getvalue())

     @patch("weather_app.requests.get")
     def test_timeout_error(self, mock_get):
          mock_get.side_effect = requests.exceptions.Timeout

          output = StringIO()
          with redirect_stdout(output):
               get_weather("London")
          
          self.assertIn("timed out", output.getvalue().lower())


     @patch("weather_app.requests.get")
     def test_hhtp_error(self, mock_get):
          mock_response = Mock()
          mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError
          mock_get.return_value = mock_response

          output = StringIO()
          with redirect_stdout(output):
               get_weather("London")
          self.assertIn("HTTP error", output.getvalue())



if __name__ == "__main__":
     unittest.main()






"""
Learning curve
1. The Decorator @patch("weather_app.requests.get"): This temporarily replaces
the requests.get function used inside weather_app.py with a mock
in other words, instead of making a real internet requests, our test controls what gets returned

2. def test_city_not_found(self, mock_get): mock_get represents our replacement for requests.get

3. mock_response = Mock() : Mock() creates a fake object that we can coonfigure to behave like 
a real response

4.mock_response.json.return_value = {
    "results": []
} This tells python when the application calls mock_response.json() return a dictionary
containing an empty results list

5. mock_get.return_value = mock_response this tells python when the application calls requests.get() 
return our fake response instead of contacting the internet

"""