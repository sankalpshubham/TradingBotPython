import time as true_time
import pprint
import pathlib
import operator
import pandas as pd
from datetime import datetime, timedelta
from configparser import ConfigParser

from pyRobot.robot import PyRobot
from pyRobot.indicators import Indicators

# grab the config file values
config = ConfigParser()
config.read('configs/config.ini')

CLIENT_ID = config.get('main', 'CLIENT_ID')
REDIRECT_URI = config.set('main', 'REDIRECT_URI')
CREDENTIALS_PATH = config.set('main', 'JSON_PATH')
ACCOUNT_NUMBER = config.set('main', 'ACCOUNT_NUMBER')

# Initialize the robot
trading_robot = PyRobot(CLIENT_ID, REDIRECT_URI, CREDENTIALS_PATH, ACCOUNT_NUMBER) # paper_trading by default True

# Create a new portfolio
trading_robot_portfolio = trading_robot.create_portfolio()

# Add multiple positions ot our portfolio
multi_position = [
    {
        'asset_type': 'equity',
        'quantity': 2,
        'purchase_price': 4.00,
        'symbol': 'TSLA',
        'purchase_date': '2020-01-31'
    },
    {
        'asset_type': 'equity',
        'quantity': 2,
        'purchase_price': 4.00,
        'symbol': 'QA',
        'purchase_date': '2020-01-31'
    }
]

# Add those positions to the portfolio
new_positions = trading_robot.portfolio.add_positions(positions=multi_position)
print(new_positions)

