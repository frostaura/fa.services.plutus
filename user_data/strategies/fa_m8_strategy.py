import numpy as np
import pandas as pd
from pandas import DataFrame
from freqtrade.strategy.interface import IStrategy
from freqtrade.strategy import (IntParameter, IStrategy, CategoricalParameter)
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

class FrostAuraM8Strategy(IStrategy):
    """
    This is FrostAura's mark 8 strategy which aims to make purchase decisions
    based on the RSI & overall performance of the asset from it's previous candlesticks.
    
    Last Optimization:
        Profit %        : 11.09%
        Optimized for   : Last 45 days, 4h
        Avg             : 5d 3h 0m
    """
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 2

    # Minimal ROI designed for the strategy.
    minimal_roi = {
        "0": 0.35,
        "787": 0.249,
        "1500": 0.086,
        "6522": 0
    }

    # Optimal stoploss designed for the strategy.
    stoploss = -0.239

    # Trailing stoploss
    trailing_stop = False

    # Optimal ticker interval for the strategy.
    timeframe = '4h'

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = False

    # These values can be overridden in the "ask_strategy" section in the config.
    use_sell_signal = True
    sell_profit_only = False
    ignore_roi_if_buy_signal = False

    # Number of candles the strategy requires before producing valid signals.
    startup_candle_count: int = 30

    # Optional order type mapping.
    order_types = {
        'buy': 'market',
        'sell': 'market',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    # Optional order time in force.
    order_time_in_force = {
        'buy': 'gtc',
        'sell': 'gtc'
    }

    plot_config = {
        'main_plot': {
            'tema': {},
            'sar': {'color': 'white'},
        },
        'subplots': {
            "MACD": {
                'macd': {'color': 'blue'},
                'macdsignal': {'color': 'orange'},
            },
            "RSI": {
                'rsi': {'color': 'red'},
            }
        }
    }

    def informative_pairs(self):
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # RSI
        dataframe['rsi'] = ta.RSI(dataframe)

        return dataframe

    buy_rsi = IntParameter([20, 80], default=38, space='buy')
    buy_rsi_direction = CategoricalParameter(['<', '>'], default='<', space='buy')

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        minimum_coin_price = 0.0000015

        dataframe.loc[
            (
                (dataframe['rsi'] < self.buy_rsi.value if self.buy_rsi_direction.value == '<' else dataframe['rsi'] > self.buy_rsi.value) &
                (dataframe['close'] > minimum_coin_price)
            ),
            'buy'] = 1

        return dataframe

    sell_rsi = IntParameter([20, 80], default=75, space='sell')
    sell_rsi_direction = CategoricalParameter(['<', '>'], default='>', space='sell')
    sell_percentage = IntParameter([1, 50], default=36, space='sell')

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        previous_close = dataframe['close'].shift(1)
        current_close = dataframe['close']
        percentage_price_delta = ((previous_close - current_close) / previous_close) * -100
        
        dataframe.loc[
            (
                (dataframe['rsi'] < self.sell_rsi.value if self.sell_rsi_direction.value == '<' else dataframe['rsi'] > self.sell_rsi.value) |
                (percentage_price_delta > self.sell_percentage.value)
            ),
            'sell'] = 1
        
        return dataframe