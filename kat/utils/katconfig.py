import json
import logging
import os


def __load_config():
    cfg_file = os.getenv('kat_cfg_file')

    logger = logging.getLogger('kat config loader')

    assert cfg_file is not None

    logger.info(f'Loading configuration from {cfg_file}')

    class Config(object):
        def __init__(self):
            with open(cfg_file, 'r') as json_file:
                config = json.load(json_file)

            for key in config.keys():
                assert all(x not in key for x in (' ', '-', ','))

                self.__setattr__(key, config[key])

    return Config()


config = __load_config()