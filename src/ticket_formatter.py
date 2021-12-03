import json
import requests
import time
import base64

from constants import Constants
from configparser import ConfigParser


class ReadConfig:
    """
    Reads essential config imformation from .ini file and returns dictionary containing necessary i
    information
    """

    def __init__(self):
        self.config_dict = {}

    def read_config_information(self):
        """
        Reads from a config file and returns config dictionary
        :return: config_dict dictionary containing necessary config information
        """
        try:
            config = ConfigParser()
            config.read(Constants.CONFIG_FILE.value)
            self.config_dict["user"] = config.get('default', 'email')
            self.config_dict["psd"] = base64.b64decode(config.get('default', 'psd')).decode('ascii')  # psd is stored in base64 encoded format
            self.config_dict["subdomain"] = config.get('default', 'subdomain')
            return self.config_dict

        except Exception as exp:
            print(f"Make sure {Constants.CONFIG_FILE.value} file is present with correct details and psd is in base64 encoded format")
            print(f"Exception raised while reading config file")
            raise


class GetTicketJson:

    def __init__(self):
        self.read_config_object = ReadConfig()


    def get_all_tickets_json(self, limit_per_page, page_specific_url=None):
        try:
            config_dict = self.read_config_object.read_config_information()
            _get_all_tickets_url_initial = f"https://{config_dict['subdomain']}.zendesk.com/api/v2/tickets.json?page[size]={limit_per_page}"
            _api_auth = config_dict["user"], config_dict["psd"]

            # url for next and previous pages 
            if page_specific_url is not None:
                url = page_specific_url
            else:
                url = _get_all_tickets_url_initial

            response = requests.get(url=url, auth=_api_auth)

            if response.status_code == 200:
                data = json.loads(response.text)
                return data
            elif response.status_code == 404:
                print("Requested records not found")
                return 404
            elif response.status_code == 401:
                print("Unauthorized, please check if your credentials are correct")
                return 401
            else:
                print("Request failed. Please check and try again\n")
                time.sleep(3)


        except Exception as exp:
            print(f"Exception raised while calling Zendesk API: {exp}")
            raise

    def get_specific_ticket_json(self, id):
        """
        Getting data for a specific ticket id
        :param id: id of the job
        :return: data of the json returned
        """
        try:
            config_dict = self.read_config_object.read_config_information()
            _get_all_tickets_url = f"https://{config_dict['subdomain']}.zendesk.com/api/v2/tickets/{id}.json"
            _api_auth = config_dict["user"], config_dict["psd"]
            response = requests.get(url=_get_all_tickets_url, auth=_api_auth)

            if response.status_code == 200:
                data = json.loads(response.text)
                return data
            elif response.status_code == 404:
                print("Requested record not found")
                return 404
            elif response.status_code == 401:
                print("Unauthorized, please check if your credentials are correct")
                return 401
            else:
                print("Request failed. Please check and try again\n")
                time.sleep(3)

        except Exception as exp:
            print(f"Exception raised while calling Zendesk API for a specific ticket: {exp}")
            raise


if __name__ == "__main__":
    rconfig_obj = ReadConfig()
    print(rconfig_obj.read_config_information())
    get_ticket_obj = GetTicketJson()
    print(get_ticket_obj.get_all_tickets_json(limit_per_page=25, page=2))
    print(get_ticket_obj.get_specific_ticket_json(id=2))


