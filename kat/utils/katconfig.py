from kat.utils import helpers
import json
from kat.utils.helpers import is_pythonic_ident
import logging
import os



print(dir(helpers))

def __load_config():
    cfg_file = os.getenv('kat_cfg_file')

    logger = logging.getLogger(f'CFG loader for {cfg_file}')

    assert cfg_file is not None

    logger.info(f'Loading configuration from {cfg_file}')

    class Config(object):
        def __init__(self):
            with open(cfg_file, 'r') as json_file:
                _config = json.load(json_file)

            for key in _config.keys():
                # Ensure that none of the keys contain strange or illegal characters.
                if not is_pythonic_ident(key):
                    logger.error(f'In \'{cfg_file}\', key \'{key}\' contains illegal characters, or is a Python3.6 '
                                 'reserve word. Please fix this and try again!')
                    exit(2)

                self.__setattr__(key, _config[key])

    return Config()


config = __load_config()
