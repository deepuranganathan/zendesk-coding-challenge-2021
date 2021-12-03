import unittest
from unittest.mock import patch
import requests
import unittest.mock
import ticket_formatter
import ticket_handler

class MockConfigClass:

    def __init__(self, mock_dict):
        self.dict = mock_dict

    def get(self, section, key):
        return self.dict.get(key)

    def read(self, test_file):
        pass

class TestTicketHandler(unittest.TestCase):

    def setUp(self) -> None:
        self.config_dict = {"email":"sample_email@gmail.com", "psd":"bmV3X3N0cmluZw==", "subdomain":"zcctestdomain"}

    @patch('ticket_formatter.ConfigParser')
    def test_read_config(self, mock_config_parser):
        mock_config_parser.return_value = MockConfigClass(self.config_dict)
        test_read_config_object = ticket_formatter.ReadConfig()
        test_dict = test_read_config_object.read_config_information()
        print("test dictionary")
        print(test_dict)
        assert test_dict['user'] == "sample_email@gmail.com"

    @patch('ticket_formatter.ConfigParser')
    def test_read_config_failure(self, mock_config_parser):
        mock_config_parser.return_value = Exception("Sample test exception")

        with self.assertRaises(Exception):
            test_read_config_object = ticket_formatter.ReadConfig()
            test_dict = test_read_config_object.read_config_information()



if __name__ == "__main__":
    unittest.main()
