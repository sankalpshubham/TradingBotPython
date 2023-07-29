import json
import pprint
import pandas as pd
import operator

from datetime import datetime, timedelta
from configparser import ConfigParser

from pyRobot.robot import PyRobot
from pyRobot.indicators import Indicators
from pyRobot.trades import Trade

# Read the Config File
config = ConfigParser()
config.read("config/config.ini")

# Read the different values
CLIENT_ID = config.get("main", "CLIENT_ID")
REDIRECT_URI = config.get("main", "REDIRECT_URI")
CREDENTIALS_PATH = config.get("main", "JSON_PATH")
ACCOUNT_NUMBER = config.get("main", "ACCOUNT_NUMBER")

# Initialize the PyRobot Object
trading_robot = PyRobot(
    client_id=CLIENT_ID,
    redirect_uri=REDIRECT_URI,
    credentials_path=CREDENTIALS_PATH,
    trading_account=ACCOUNT_NUMBER,
    paper_trading=True
)

# Create a new portfolio
trading_robot_portfolio = trading_robot.create_portfolio()

# Define trading Symbol
trading_symbol = "FCEL"

trading_robot.portfolio.add_position(
    symbol=trading_symbol,
    asset_type='equity'
)

# Grab the historical prices, first define the start and end date
end_date = datetime.today()                 # end point for pulling data
start_date = end_date - timedelta(days=30)  # start pulling for 30 days ago

# Grab historical prices
historical_prices = trading_robot.grab_historical_prices(
    start=end_date,
    end=start_date,
    bar_size=1,   # One day bars only!
    bar_type='minute'
)

# Conver the data to a Stock Frame
stock_frame = trading_robot.create_stock_frame(data=historical_prices['aggregated'])

# Print the head of the StockFrame
pprint.pprint(stock_frame.frame.head())

# Add the stock frame to the portfolio
trading_robot.portfolio.stock_frame = stock_frame
trading_robot.portfolio.historical_prices = historical_prices

# Inidicators (our strategy is we want a 200 moving avg and 50 day moving avg)
indicator_client = Indicators(price_data_frame=stock_frame)

# Add the 200-day SMA
indicator_client.sma(period=200, column_name='sma_200')
# Add the 50-day SMA
indicator_client.sma(period=50, column_name='sma_50')

# Add the 50-day EMA
indicator_client.ema(period=50, column_name="ema")
# print(stock_frame.frame.head())
# print(stock_frame.frame.tail())




