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
            print(f"File {Constants.CONFIG_FILE.value} might not be present")
            print(f"Exception raised while reading config file: {exp}")


class GetTicketJson(ReadConfig):

    def get_all_tickets_json(self, limit_per_page, page=1):
        try:
            config_dict = self.read_config_information()
            _get_all_tickets_url  = f"https://{config_dict['subdomain']}.zendesk.com/api/v2/tickets.json?page[size]={limit_per_page}"
            _api_auth = config_dict["user"], config_dict["psd"]
            response = requests.get(url=_get_all_tickets_url, auth=_api_auth)

            if response.status_code == 200:
                data = json.loads(response.text)
                return data
            elif response.status_code == 404:
                print("Requested URL not found")
            elif response.status_code == 400:
                print("Unauthorized, please check if your credentials are correct")
            else:
                print("Request failed. Please check and try again\n")
                time.sleep(3)

        except Exception as exp:
            print(f"Exception raised while calling Zendesk API: {exp}")

    def get_specific_ticket_json(self, id):
        """
        Getting data for a specific ticket id
        :param id: id of the job
        :return: data of the json returned
        """
        try:
            config_dict = self.read_config_information()
            _get_all_tickets_url = f"https://{config_dict['subdomain']}.zendesk.com/api/v2/tickets/{id}.json"
            _api_auth = config_dict["user"], config_dict["psd"]
            response = requests.get(url=_get_all_tickets_url, auth=_api_auth)

            if response.status_code == 200:
                data = json.loads(response.text)
                return data
            elif response.status_code == 404:
                print("Requested URL not found")
            elif response.status_code == 400:
                print("Unauthorized, please check if your credentials are correct")
            else:
                print("Request failed. Please check and try again\n")
                time.sleep(3)

        except Exception as exp:
            print(f"Exception raised while calling Zendesk API for a specific ticket: {exp}")


if __name__ == "__main__":
    rconfig_obj = ReadConfig()
    print(rconfig_obj.read_config_information())
    get_ticket_obj = GetTicketJson()
    print(get_ticket_obj.get_all_tickets_json(limit_per_page=25, page=2))
    print(get_ticket_obj.get_specific_ticket_json(id=2))


