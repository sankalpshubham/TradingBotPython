import pandas as pd
from td.client import TDClient
#from td.utils import milliseconds_since_epoch

from datetime import datetime, time, timezone

from typing import List, Dict, Union
from pyRobot.portfolio import Portfolio

class PyRobot():
    def __init__(self, client_id: str, redirect_uri: str, credentials_path: str = None, trading_account: str = None, paper_trading: bool = True) -> None:
        self.trading_account: str = trading_account     
        self.client_id: str = client_id
        self.credentials_path: str = credentials_path
        self.redirect_uri: str = redirect_uri
        self.session: TDClient = self._create_session()     # called from different function (private)
        self.trades: dict = {}
        self.historical_prices: dict = {}
        self.stock_frame = None
        self.paper_trading = paper_trading


    def _create_session(self) -> TDClient:
        """Create a new session with the specified account."""

        td_client = TDClient (              # instance of the client
            client_id = self.client_id,
            redirect_uri = self.redirect_uri,
            credentials_path = self.credentials_path
        )

        # login to the session
        td_client.login()
        return td_client
    
    # is the market open or not (check for weekends/holidies/closed day) (this is US market)
    @property
    def pre_market_open(self) -> bool:
        pre_market_start_time = datetime.now().replace(hour=12, minute=00, second=00, tzinfo=timezone.utc).timestamp()  # current local date and time in tzinfo (returns float)
        market_start_time = datetime.now().replace(hour=13, minute=30, second=00, tzinfo=timezone.utc).timestamp()
        now = datetime.now().replace(tzinfo=timezone.utc).timestamp()

        return True if market_start_time >= now >= pre_market_start_time else False 

    @property
    def post_market_open(self) -> bool:
        post_market_end_time = datetime.now().replace(hour=22, minute=30, second=00, tzinfo=timezone.utc).timestamp()  # current local date and time in tzinfo (returns float)
        market_end_time = datetime.now().replace(hour=20, minute=00, second=00, tzinfo=timezone.utc).timestamp()
        now = datetime.now().replace(tzinfo=timezone.utc).timestamp()

        return True if post_market_end_time >= now >= market_end_time else False

    @property
    def regular_market_open(self) -> bool:
        market_start_time = datetime.now().replace(hour=13, minute=30, second=00, tzinfo=timezone.utc).timestamp()  # current local date and time in tzinfo (returns float)
        market_end_time = datetime.now().replace(hour=20, minute=00, second=00, tzinfo=timezone.utc).timestamp()
        now = datetime.now().replace(tzinfo=timezone.utc).timestamp()

        return True if market_end_time >= now >= market_start_time else False
    
    
    def create_portfolio(self):
        # Initialize a new portfolio object
        self.portfolio = Portfolio(account_number=self.trading_account)
        
        # Assign the client
        self.portfolio.td_client = self.session
        return self.portfolio

    def create_trade(self):
        pass

    def grab_current_quotes(self) -> dict:
        # First grab all the symbols
        symbols = self.portfolio.positions.keys()

        # Grab the quotes
        quotes = self.session.get_quotes(instruments=list(symbols))
        return quotes

    def grab_historical_prices(self) -> List[Dict]:
        pass

    def create_stock_frame(self):
        pass