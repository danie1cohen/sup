"""
Get configuration from your ~/.sup.yml file.
"""

FILENAME = 'sup_%s.yml'

TEMPLATE = """--- # sup? %s

"""

def read_config():
    config_path = os.path.join(os.path.expanduser('~'), '.sup.yml')

    if not os.path.exists(config_path):
        print('Could not find your sup? config file at path: %s' % config_path)
        sys.exit(1)
    else:
        with open(config_path, 'rb') as stream:
            config = yaml.load(stream)
        return config['archive_dir'], config['text_editor'], config['print_cmd']


ARCHIVE_DIR, TEXTEDITOR, PRINT_CMD = read_config()
