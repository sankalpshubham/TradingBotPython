import numpy as np
import pandas as pd

from pandas.core.groupby import DataFrameGroupBy
from pandas.core.window import RollingGroupby

from datetime import time, datetime, timezone
from typing import List, Dict, Union

class StockFrame():
    def __init__(self, data: List[dict]) -> None:
        self._data = data
        self._frame = pd.DataFrame = self.create_frame()
        self._symbol_groups: DataFrameGroupBy = None
        self._symbol_rolling_groups: RollingGroupby = None

    @property
    def frame(self) -> pd.DataFrame:
        return self._frame
    
    @property
    def symbol_groups(self) -> DataFrameGroupBy:
        self._symbol_groups = self._frame.groupby(
            by = 'symbol',
            as_index = False,
            sort = True         # very important
        )

        return self._symbol_groups
    
    def symbol_rolling_groups(self, size: int) -> RollingGroupby:
        if not self._symbol_groups:
            self.symbol_groups

        self._symbol_rolling_groups = self._symbol_groups.rolling(size)
        return self._symbol_rolling_groups
    
    def create_frame(self) -> pd.DataFrame:
        #make a data frame
        price_df = pd.DataFrame(data=self._data)
        price_df = self._parse_datatime_column(price_df=price_df)       # could merge with the seperate functions (prob not needed)
        price_df = self._set_multi_index(price=price_df)
        return price_df
    
    def _parse_datatime_column(self, price_df: pd.DataFrame) -> pd.DataFrame:
        price_df['datetime'] = pd.to_datetime(price_df['datetime'], unit='ms', origin='unix')   # this will parse a timestamp from a epoch
        return price_df
    
    def _set_multi_index(self, price_df: pd.DataFrame) -> pd.DataFrame:
        price_df = price_df.set_index(keys=['symbol', 'datetime'])
        return price_df
    
    def add_rows(self, data: dict) -> None:
        column_names = ['open', 'close', 'high', 'low', 'volume']
        
        for quote in data:
            # parse the timestamp
            time_stamp = pd.to_datetime(
                quote['datetime'],
                unit='ms',
                origin='unix'
            )

            # Define our index
            row_id = (quote['symbol'], time_stamp)

            # Define our values
            row_values = [
                quote['open'],
                quote['close'],
                quote['high'],
                quote['low'],
                quote['volume']
            ]

            # New row
            new_row = pd.Series(data=row_values)
            # Add row
            self.frame.loc[row_id, column_names] = new_row.values
            self.frame.sort_index(inplace=True)

    # defining buy and sell thresholds
    def do_indicators_exist(self, column_names: List[str]) -> bool:
        if set(column_names).issubset(self._frame.columns):
            return True
        else:
            raise KeyError("The following indicator columns are missing the StockFrame: {missing_columns}".format (
                missing_columns=set(column_names).difference(self._frame.columns)
            ))

    def _check_signals(self, indicators: dict) -> Union[pd.Series, None]:
        # Grab the last rows
        last_rows = self._symbol_groups.tail(1)

        conditions = []

        # Check to see if all the columns exist
        if self.do_indicators_exist(column_names=indicators.key()):
            for indicator in indicators:
                column = last_rows[indicator]

                buy_conditon_target = indicators[indicator]['buy']
                sell_conditon_target = indicators[indicator]['sell']

                buy_conditon_operator = indicators[indicator]['buy_operator']
                sell_conditon_operator = indicators[indicator]['sell_operator']

                condition_1: pd.Series = buy_conditon_operator(column, buy_conditon_target)
                condition_2: pd.Series = sell_conditon_operator(column, sell_conditon_target)

                condition_1: condition_1.where(lambda x: x == True).dropna()
                condition_2: condition_2.where(lambda x: x == True).dropna()

                conditions.append(("buys", condition_1), ("sells", condition_2))

        return conditions