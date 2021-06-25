import numpy as np
import pandas as pd
from pandas import DataFrame
from freqtrade.strategy.interface import IStrategy
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

class FrostAuraM8Strategy(IStrategy):
    """
    This is FrostAura's mark 8 strategy which aims to make purchase decisions
    based on the RSI & overall performance of the asset from it's previous candlesticks.
    
    Last Optimization:
        Profit %        : 84.69%
        Optimized for   : Last 30 days, 4h
        Avg             : 160.0 m
    """
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 2

    # Minimal ROI designed for the strategy.
    minimal_roi = {
        "0": 0.7218,
        "758": 0.21619,
        "1864": 0.07295,
        "6108": 0
    }

    # Optimal stoploss designed for the strategy.
    stoploss = -0.02059

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

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        var_rsi = 88
        minimum_coin_price = 0.0000015

        dataframe.loc[
            (
                (dataframe['rsi'] > var_rsi) &
                (dataframe['close'] > minimum_coin_price)
            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        var_sell_rsi = 37
        var_sell_percentage = 23
        
        previous_close = dataframe['close'].shift(1)
        current_close = dataframe['close']
        percentage_price_delta = ((previous_close - current_close) / previous_close) * -100
        
        dataframe.loc[
            (
                (dataframe['rsi'] < var_sell_rsi) |
                (percentage_price_delta > var_sell_percentage)
            ),
            'sell'] = 1
        
        return dataframe