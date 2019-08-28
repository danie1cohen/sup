"""
Get configuration from your ~/.sup.yml file.
"""
import logging
import os

import yaml


logger = logging.getLogger(__name__)


FILENAME = os.environ.get('SUP_FILENAME', 'sup_%s.yml')

CONFIG_PATH = os.environ.get(
    'SUP_CONFIG',
    os.path.join(os.path.expanduser('~'), '.sup.yml')
)

TEMPLATE = """--- # sup? %s

"""


def read_config(config_path, autocreate=False, **kwargs):
    """
    Read and return the sup configuration.
    """
    if not os.path.exists(config_path):
        print('Could not find your sup? config file at path: %s' % config_path)
        create_config(config_path, **kwargs) if autocreate else sys.exit(1)

    print('Reading config from %s' % config_path)

    with open(config_path, 'rb') as stream:
        config = yaml.load(stream)

    params = config['archive_dir'], config['text_editor'], config['print_cmd']
    print('config: %s' % config)
    return config


def create_config(config_path, **kwargs):
    config = {
        'archive_dir': os.path.join(os.path.expanduser('~'), 'sup'),
        'text_editor': 'vim',
        'print_cmd': 'cat',
    }
    print('default config %s' % config)


    with open(config_path, 'wb') as stream:
        config.update(kwargs)
        print('updated config %s' % config)
        stream.write(yaml.dump(config))

    print('Created new sup? config with contents %s' % config)
    return config

CONFIG = read_config(CONFIG_PATH)

ARCHIVE_DIR = CONFIG['archive_dir']
TEXTEDITOR = CONFIG['text_editor']
PRINT_CMD = CONFIG['print_cmd']
