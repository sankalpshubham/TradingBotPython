from datetime import datetime

from typing import List, Union, Optional

class Trade():
    def __init__(self):
        self.order = {}
        self.trade_id = ""

        self.side = ""              # whether going long or short
        self.side_opposite = ""     # opposite range
        self.enter_or_exit = ""     # enter position / exit position (long/short)
        self.enter_or_exit_opposite = ""

        self._order_response = {}   # api sends info back to us everytime we submit an order
        self.triggered_added = False
        self._multi_leg = False     # for multi leg order
        

    def new_trade(self, trade_id: str, order_type: str, side: str, enter_or_exit: str, price: float = 0.00, stop_limit_price: float = 0.00) -> dict:
        self.trade_id = trade_id
        self.order_type = {
            "mrkt": "MARKET",
            "lmt":  "LIMIT",
            "stop":"STOP",
            "stop_lmt": "STOP_LIMIT",
            "trailing_stop": "TRAILING_STOP"
        }

        self.order_instructions = {
            'enter': {
                'long': 'BUY',
                'short':'SELL_SHORT'
            },
            'exit': {
                'long': 'SELL',
                'short': 'BUY_TO_COVER'
            }
        }

        self.order = {
            "orderStrategyType": "SINGLE",
            "orderType": self.order_type[order_type],
            "session": "NORMAL",    # day only? what about other sessions like AM and PM etc..
            "dudration": "DAY",
            "orderLegCollection": [
                {
                    "instruction": "self.order_instructions[enter_or_exit][side]",
                    "quantity": 0,
                    "instrument": {
                        "symbol": None,
                        "assetType": None      # EQTY OR FUTURES
                    }
                }
            ]
        }

        if self.order['orderType'] == "STOP":
            self.order['stopPrice'] = price
        elif self.order['orderType'] == "LIMIT":
            self.order['price'] = price
        elif self.order['orderType'] == "STOP_LIMIT":
            self.order['stopPrice'] = price
            self.order['price'] = stop_limit_price
        elif self.order['orderType'] == "TRAILING_STOP":
            self.order['stopPriceLinkBasis'] = ""
            self.order['stopPriceLinkType'] = ""
            self.order['stopPriceOffset'] = 0.00
            self.order['stopType'] = 'STANDARD'

        self.enter_or_exit = enter_or_exit
        self.side = side
        self.order_type = order_type
        self.price = price

        # store info for later use
        if order_type == "stop":
            self.stop_price = price
        elif order_type == "stop-lmt":
            self.stop_price = price
            self.stop_limit_price = stop_limit_price
        else:
            self.stop_price = 0.0

        if self.enter_or_exit == 'enter':
            self.enter_or_exit_opposite = 'exit'
        elif self.enter_or_exit == 'exit':
            self.enter_or_exit_opposite = 'enter'

        if self.side == 'long':
            self.side_opposite = 'short'
        elif self.side == 'short':
            self.side_opposite = 'long'

        return self.order

    def instrument(self, symbol: str, quantity: int, asset_type: str, sub_asset_type: str = None, order_leg_id: int = 0) -> dict:
        leg = self.order['orderLegCollection'][order_leg_id]
        leg['instrument']['symbol'] = symbol
        leg['instrument']['assetType'] = asset_type
        leg['quantity'] = quantity

        self.order_size = quantity
        self.symbol = symbol
        self.asset_type = asset_type

        return leg
    
    def good_till_cancel(self, cancel_time: datetime) -> None:
        self.order['duration'] = 'GOOD_TILL_CANCEL'
        self.order['cancelTime'] = cancel_time.isoformat()

    def modify_side(self, side: Optional[str], order_leg_id: int = 0) -> None:
        if side and side not in ['buy', 'sell', 'sell_short', 'buy_to_cover']:
            raise ValueError("You passed through an invalid side")
        
        if side:
            self.side['orderLegCollection'][order_leg_id]['instructions'] = side.upper()
        else:
            self.order['orderLegCollection'][order_leg_id]['instructions'] = self.order_instructions[self.enter_or_exit][self.side_opposite]

    def add_box_range(self, profit_size: float = 0.00, percentage: bool = False, stop_limit: bool = False):
        if not self.triggered_added:
            self._convert_to_trigger()

        self.add_take_profit(profit_size=profit_size, percentage=percentage)

        if not stop_limit:
            self.add_stop_loss(stop_size=profit_size, percentage=percentage)


    def _convert_to_trigger(self):
        pass

    def add_take_profit(self):
        pass

    def add_stop_loss(self):
        pass