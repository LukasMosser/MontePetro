__author__ = 'lmosser'
import json

class JSONParser(object):
    def __init__(self, file_name):
        json_data = open(file_name)
        self.data = json.load(json_data)
        if self.validate_json():
            self.regions = [region for region in self.data["Regions"]]
            self.properties = [property for property in self.data["Properties"]]

    def validate_json(self, verbose=False):
        valid = True
        try:
            name = self.data["Name"]
        except KeyError:
            if verbose:
                print "No attribute Name in configuration file."
            valid = False

        try:
            version = self.data["Version"]
        except KeyError:
            if verbose:
                print "No attribute Version in configuration file."
            valid = False
        try:
            author = self.data["Author"]
        except KeyError:
            if verbose:
                print "No attribute Author in configuration file."
            valid = False

        try:
            regions = self.data["Regions"]
            if len(regions) is 0:
                valid = False
                if verbose:
                    print "No Regions defined."
        except KeyError:
            if verbose:
                print "No attribute Regions in configuration file."
            valid = False

        try:
            properties = self.data["Properties"]
            if len(properties) is 0:
                valid = False
                if verbose:
                    print "No Properties defined."
        except KeyError:
            if verbose:
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
            if verbose:
                print "Property in region not defined in Properties section."

        return valid