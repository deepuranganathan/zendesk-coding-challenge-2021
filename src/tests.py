from unittest.mock import patch
import unittest.mock
import ticket_formatter
import ticket_handler
import main_view

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


class MockGetTicketJson:

    def __init__(self):
        pass

    def get_specific_ticket_json(self, ticket_id):
        return {"ticket":{"url":"https://zccdeepak.zendesk.com/api/v2/tickets/2.json","id":2,"external_id":None,"via":{"channel":"api","source":{"from":{},"to":{},"rel":None}},"created_at":"2021-11-30T10:19:56Z","updated_at":"2021-11-30T10:19:56Z","type":None,"subject":"velit eiusmod reprehenderit officia cupidatat","raw_subject":"velit eiusmod reprehenderit officia cupidatat","description":"Aute ex sunt culpa ex ea esse sint cupidatat aliqua ex consequat sit reprehenderit. Velit labore proident quis culpa ad duis adipisicing laboris voluptate velit incididunt minim consequat Nonea. Laboris adipisicing reprehenderit minim tempor officia ullamco occaecat ut laborum.\n\nAliquip velit adipisicing exercitation irure aliqua qui. Commodo eu laborum cillum nostrud eu. Mollit duis qui non ea deserunt est est et officia ut excepteur Lorem pariatur deserunt.","priority":None,"status":"open","recipient":None,"requester_id":1267183841729,"submitter_id":1267183841729,"assignee_id":1267183841729,"organization_id":1900082707364,"group_id":4411521016859,"collaborator_ids":[],"follower_ids":[],"email_cc_ids":[],"forum_topic_id":None,"problem_id":None,"has_incidents":False,"is_public":True,"due_at":None,"tags":["est","incididunt","nisi"],"custom_fields":[],"satisfaction_rating":None,"sharing_agreement_ids":[],"fields":[],"followup_ids":[],"ticket_form_id":1900004329304,"brand_id":1900001366364,"allow_channelback":False,"allow_attachments":True}}
    
    def get_all_tickets_json(self, limit_per_page, page_specific_url):
        return {"tickets":[{"url":"https://zccdeepak.zendesk.com/api/v2/tickets/1.json","id":1,"external_id":None,"via":{"channel":"sample_ticket","source":{"from":{},"to":{},"rel":None}},"created_at":"2021-11-30T09:58:20Z","updated_at":"2021-11-30T09:58:21Z","meta":{"has_more":True},"type":"incident","subject":"Sample ticket: Meet the ticket","raw_subject":"Sample ticket: Meet the ticket","description":"Hi there,\n\nI’m sending an email because I’m having a problem setting up your new product. Can you help me troubleshoot?\n\nThanks,\n The Customer\n\n","priority":"normal","status":"open","recipient":None,"requester_id":1902381585344,"submitter_id":1267183841729,"assignee_id":1267183841729,"organization_id":None,"group_id":4411521016859,"collaborator_ids":[],"follower_ids":[],"email_cc_ids":[],"forum_topic_id":None,"problem_id":None,"has_incidents":False,"is_public":True,"due_at":None,"tags":["sample","support","zendesk"],"custom_fields":[],"satisfaction_rating":None,"sharing_agreement_ids":[],"followup_ids":[],"ticket_form_id":1900004329304,"brand_id":1900001366364,"allow_channelback":False,"allow_attachments":True}],"links":{"prev":"dample_url", "next":"sample_url"},"meta":{"has_more":True}}
        


class TestTicketFormatter(unittest.TestCase):

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


class TestTicketHandler(unittest.TestCase):

    @patch('ticket_handler.GetTicketJson')
    @patch('ticket_handler.input', create=True)
    def test_read_config(self, mock_input, mock_get_ticket_json):
        mock_input.side_effect = ['1', '3','1','2','4']
        mock_get_ticket_json.return_value = MockGetTicketJson()
        ticket_handler_obj = ticket_handler.Ticket()
        with self.assertRaises(SystemExit):
            ticket_handler_obj.get_specific_ticket_handler()

        with self.assertRaises(SystemExit):
            ticket_handler_obj.get_paged_tickets()


class MockTicket:

    def __init__(self):
        pass

    def get_specific_ticket_handler(self):
        pass

    def get_paged_tickets(self):
        pass

class TestMainMenu(unittest.TestCase):

    @patch('main_view.input', create=True)
    @patch('main_view.Ticket')
    def test_main_menu(self, mock_ticket, mock_input):
        mock_input.side_effect = ['1', '2', '5', 'q']
        main_view_obj = main_view.MainMenu()
        print(main_view_obj)
        repr(main_view_obj)
        with self.assertRaises(SystemExit):
            main_view_obj.menu()














if __name__ == "__main__":
    unittest.main()
