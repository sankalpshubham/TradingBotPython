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

# Add a single position to the portfolio
trading_robot.portfolio.add_position (
    symbol='MSFT',
    quantity=10,
    purchase_price=598.76,
    asset_type='equity',
    purchase_date="2020-01-31"
)
pprint.pprint(trading_robot.portfolio.positions)


# check to see if the regular market is open
if trading_robot.regular_market_open:
    print("Regular Market Open")
else:
    print("Regular Market Not Open")

# check to see if the pre market is open
if trading_robot.pre_market_open:
    print("Pre Market Open")
else:
    print("Pre Market Not Open")
 
# check to see if the post market is open
if trading_robot.post_market_open:
    print("Post Market Open")
else:
    print("Post Market Not Open")
 
# Grab the current quotes form the portfolio
current_quotes = trading_robot.grab_current_quotes()
pprint.pprint(current_quotes)

# Define our date range
end_date = datetime.today()                 # end point for pulling data
start_date = end_date - timedelta(days=30)  # start pulling for 30 days ago

# Grab historical prices
historical_prices = trading_robot.grab_historical_prices(
    start=start_date,
    end=end_date,
    bar_size=1,   # One day bars only!
    bar_type='minute'
)

# Convert data into a StockFrame
stock_frame = trading_robot.create_stock_frame(data=historical_prices['aggregated'])

# Print the head of the StockFrame
pprint.pprint(stock_frame.frame.head(n=20))

# Create a new Trade obj
new_trade = trading_robot.create_trade(
    trade_id='long_msft',
    enter_or_exit='enter',
    long_or_short='long',
    order_type='lmt',
    price=458.97,      # set limit at $458.
)

# Make it Good Till Cancel
new_trade.good_till_cancel(cancel_time=datetime.now() + timedelta(minutes=90))  # only good till 90 mins from now

# Change the session
new_trade.modify_session(session='am')

# Add an Order Leg
new_trade.instrument(
    symbol='MSFT',
    quantity=2,
    asset_type='EQUITY'
)

# Add a Stop Loss Order with the Main Order
new_trade.add_stop_loss(
    stop_price=.10,         # 10 cents below current price (calculating abs value not percentage of value)
    percentage=False
)

# Print out the order
pprint.pp
(new_trade.order)
