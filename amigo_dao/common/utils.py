import yaml
import os

absolute_path = os.path.dirname(os.path.abspath(__file__))
file_path = absolute_path + '/config/config.yaml'

def read_config_file():
    """
    Read the config.yaml file

    """
    with open(file_path) as file:
        config_data = yaml.safe_load(file)
    return config_data

