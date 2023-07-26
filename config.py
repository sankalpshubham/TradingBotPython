import os
from configparser import ConfigParser

config = ConfigParser()

# we set the credentials here
config.add_section('main')
config.set('main', 'CLIENT_ID', '')
config.set('main', 'REDIRECT_URI', '')
config.set('main', 'JSON_PATH', '')
config.set('main', 'ACCOUNT_NUMBER', '')

# Check if the config file directory exists
if not os.path.exists('configs'):
    os.mkdir('configs')

# Write the config file
with open('configs/config.ini', 'w+') as f:
    config.write(f)
