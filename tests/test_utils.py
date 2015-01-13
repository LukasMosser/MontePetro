__author__ = 'lmosser'
from montepetro.properties import Property

def mock_random():
    return 1.0

def mock_numerical_function():
    return 1.0


class MockProperty(Property):
    def __init__(self):
        Property.__init__(self, name="MockProperty", desc="A Mock Property")

    def generate_values(self):
        return True
