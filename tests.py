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

class MockReadConfig:

    def __init__(self):
        pass

    def read_config_information(self):
        return {"user": "sample_email@zendesk.com", "psd":"bmV3X3N0cmluZw==", "subdomain":"zcctestdomain"}

class MockResponse:

    def __init__(self, status_code):
        self.status_code = status_code
        self.text = '{"test":"testval"}'

    def json(self):
        response_dict = {"test_key":"test_val"}
        return response_dict


class TestTicketHandler(unittest.TestCase):

    def setUp(self) -> None:
        self.config_dict = {"email":"sample_email@zendesk.com", "psd":"bmV3X3N0cmluZw==", "subdomain":"zcctestdomain"}

    @patch('ticket_formatter.ConfigParser')
    def test_read_config(self, mock_config_parser):
        mock_config_parser.return_value = MockConfigClass(self.config_dict)
        test_read_config_object = ticket_formatter.ReadConfig()
        test_dict = test_read_config_object.read_config_information()
        assert test_dict['user'] == "sample_email@zendesk.com"

    @patch('ticket_formatter.ConfigParser')
    def test_read_config_failure(self, mock_config_parser):
        mock_config_parser.return_value = Exception("Sample test exception")

        with self.assertRaises(Exception):
            test_read_config_object = ticket_formatter.ReadConfig()
            test_dict = test_read_config_object.read_config_information()

    @patch('ticket_formatter.ReadConfig')
    @patch('ticket_formatter.requests.get')
    def test_get_ticket_json(self, mock_request_get, mock_read_config):
        mock_read_config.return_value = MockReadConfig()
        mock_request_get.return_value = MockResponse(status_code=200)

        ticket_json_obj = ticket_formatter.GetTicketJson()
        correct_response_data = ticket_json_obj.get_all_tickets_json(limit_per_page=25)

        correct_response_data_single = ticket_json_obj.get_specific_ticket_json('23')

        # for 404 records
        mock_request_get.return_value = MockResponse(status_code=404)

        response_data_404 = ticket_json_obj.get_all_tickets_json(limit_per_page=25)

        reponse_404 = ticket_json_obj.get_specific_ticket_json('2366')

        # for 401 (unauthorised)

        mock_request_get.return_value = MockResponse(status_code=401)

        response_data_401 = ticket_json_obj.get_all_tickets_json(limit_per_page=25)

        reponse_401 = ticket_json_obj.get_specific_ticket_json('2366')

        assert correct_response_data['test'] == 'testval'






if __name__ == "__main__":
    unittest.main()
