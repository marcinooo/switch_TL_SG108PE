import os
from dotenv import load_dotenv


def set_up_environment_variables():
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    env_file = os.path.join(current_file_dir, '..', '..', 'environment', '.env.testing')
    load_dotenv(env_file)
