from amigo_dao.common.utils import read_config_file 
config = read_config_file()

user_info = config["TABLES"]["user_info"]
user_scores = config["TABLES"]["user_scores"]
user_login = config["TABLES"]["user_login"]
user_files = config["TABLES"]["user_files"]
