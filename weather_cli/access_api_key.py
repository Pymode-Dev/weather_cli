from configparser import ConfigParser


def get_api_info():
    filepath = "./secrets.ini"
    config_parser = ConfigParser()
    config_parser.read(filepath)
    return config_parser
