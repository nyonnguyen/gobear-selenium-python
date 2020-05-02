import yaml
import os
import shutil
import datetime


def read_yaml(file_name):
    with open(os.path.dirname(__file__).replace('Utilities', file_name)) as f:
        return yaml.safe_load(f)


def gen_file_name(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return os.path.join(path, str(datetime.datetime.now().timestamp()) + '.png')


def remove_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path, True)