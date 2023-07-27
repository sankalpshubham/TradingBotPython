from typing import List, Dict, Union, Optional, Tuple
from td.client import TDClient

class Portfolio():
    def __init__(self, account_number: Optional[str]):
        self.account_number = account_number
        self.positions = {}
        self.positions_count = 0
        self.market_value = 0.0
        self.profit_loss = 0.0
        self.risk_tolerance = 0.0
        self._td_client: TDClient = None

    # to add one position
    def add_position(self, symbol: str, asset_type: str, purchase_date: Optional[str], quantity: int = 0, purchase_price: float = 0.0) -> dict:
        self.positions[symbol] = {}
        self.positions[symbol]['symbol'] = symbol
        self.positions[symbol]['quantity'] = quantity
        self.positions[symbol]['purchase_price'] = purchase_price
        self.positions[symbol]['purchase_date'] = purchase_date
        self.positions[symbol]['asset_type'] = asset_type

        return self.positions
    
    # to add multiple positions
    def add_positions(self, positions: List[dict]) -> dict:
        if isinstance(positions, list):
            for position in positions:
                self.add_position(
                    symbol = position['symbol'],
                    asset_type = position['asset_type'],
                    purchase_date = position.get('purchase_date', None),
                    purchase_price = position.get('purchase_price', 0.0),
                    quantity = position.get('quantity', 0) 
                )
                return self.positions
        else:
            raise TypeError("Positions must be a list of dictionary")
    
    def remove_position(self, symbol: str) -> Tuple[bool, str]:
        if symbol in self.positions:
            del self.positions[symbol]
            return (True, "{Symbol} was successfully removed.".format(symbol=symbol))
        else:
            return (False, "{Symbol} did not exist in the portfolio.".format(symbol=symbol))


    def in_portfolio(self, symbol: str) -> bool:
        return True if symbol in self.positions else False
    
    def is_profitable(self, symbol: str, current_price: float) -> bool:
        "get the pruchase price"
        purchase_price = self.positions[symbol]['purchase_price']
        return True if purchase_price <= current_price else False

    @property
    def td_client(self) -> TDClient:
        return self._td_client

    @td_client.setter
    def td_client(self, td_client: TDClient) -> None:
        self._td_client: TDClient = td_client

    def set_ownership_status(self, symbol: str, ownership: bool) -> None:
        if self.in_portfolio(symbol=symbol):
            self.positions[symbol]['ownership_status'] = ownership
        else:
            raise KeyError(
                "Can't set ownership status, as you do not have the symbol in your portfolio."
            )
    
    def total_allocation(self):
        pass

    def risk_exposure(self):
        pass
    
    def total_market_value(self):
        pass