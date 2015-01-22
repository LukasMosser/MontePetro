__author__ = 'lmosser'
import json
import logging


class JSONParser(object):
    def __init__(self, file_name):
        json_data = open(file_name)
        self.data = json.load(json_data)
        if self.validate_json():
            self.regions = [region for region in self.data["Regions"]]
            self.properties = [prop for prop in self.data["Properties"]]

    def validate_json(self, verbose=False):
        valid = True
        try:
            name = self.data["Name"]
        except KeyError:
            logging.log(logging.WARNING, "No attribute Name in configuration file.")
            valid = False

        try:
            version = self.data["Version"]
        except KeyError:
            logging.log(logging.WARNING, "No attribute Version in configuration file.")
            valid = False
        try:
            author = self.data["Author"]
        except KeyError:
            logging.log(logging.WARNING, "No attribute Author in configuration file.")
            valid = False

        try:
            regions = self.data["Regions"]
            if len(regions) is 0:
                valid = False
                logging.log(logging.WARNING, "No Regions defined.")
        except KeyError:
            logging.log(logging.WARNING, "No attribute Regions in configuration file.")
            valid = False

        try:
            properties = self.data["Properties"]
            if len(properties) is 0:
                valid = False
                logging.log(logging.WARNING, "No Properties defined.")
        except KeyError:
            print "No attribute Properties in configuration file."
            valid = False

        try:
            regions = self.data["Regions"]
            for region in regions:
                properties = regions["Properties"]
                for prop in properties:
                    if prop not in self.data["Properties"]:
                        valid = False
                        raise KeyError
        except KeyError:
            logging.log(logging.WARNING, "Property in region not defined in Properties section.")

        return valid