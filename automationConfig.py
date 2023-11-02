################################################################

# File: automationConfig.py
# Author: Satyam Pandey
# Date: 2023-11-02
# Description: This is a Python script for Reading the KeyPress configuration.

################################################################
from configparser import ConfigParser

def key_config(filename='config.cfg', section="keypress"):
    """Configuration related to Logger config"""
    # create a parser
    cfgdict = {}
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            cfgdict[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )
    return cfgdict
