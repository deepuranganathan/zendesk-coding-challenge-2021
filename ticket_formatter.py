import json
import requests
import time
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
            self.config_dict["psd"] = config.get('default', 'psd')
            self.config_dict["subdomain"] = config.get('default', 'subdomain')
            return self.config_dict

        except Exception as exp:
            print(f"File {Constants.CONFIG_FILE.value} might not be present")
            print(f"Exception raised while reading config file: {exp}")



