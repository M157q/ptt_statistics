import os

from . import constants


def create_dir_if_not_exists():
    if not os.path.isdir(constants.dir_path):
        os.mkdir(constants.dir_path)
