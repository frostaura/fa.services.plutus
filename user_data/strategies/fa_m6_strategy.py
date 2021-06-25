# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# isort: skip_file
import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame
from freqtrade.strategy.interface import IStrategy
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

class FrostAuraM6Strategy(IStrategy):
    """
    This is FrostAura's mark 6 strategy which aims to make purchase decisions
    based on the ADX and MACD indicators. A momentum-based strategy.
    
    Last Optimization:
        Profit %        : -14.25%
        Optimized for   : Last 30 days, 1h
        Avg             : 990.0 m
    """
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 2

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi".
    minimal_roi = {
        "0": 0.28197,
        "196": 0.16291,
        "343": 0.04476,
        "1586": 0
    }

    # Optimal stoploss designed for the strategy.
    # This attribute will be overridden if the config file contains "stoploss".
    stoploss = -0.33028

    # Trailing stoploss
    trailing_stop = False

    # Optimal ticker interval for the strategy.
    timeframe = '1h'

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = False

    # These values can be overridden in the "ask_strategy" section in the config.
    use_sell_signal = True
    sell_profit_only = False
    ignore_roi_if_buy_signal = False

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 50

    # Optional order type mapping.
    order_types = {
        'buy': 'limit',
        'sell': 'limit',
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
        # ADX
        dataframe['adx'] = ta.ADX(dataframe)

        # Plus Directional Indicator / Movement
        dataframe['plus_di'] = ta.PLUS_DI(dataframe)

        # Minus Directional Indicator / Movement
        dataframe['minus_di'] = ta.MINUS_DI(dataframe)

        # MACD
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        minimum_coin_price = 0.0000015
        
        dataframe.loc[
            (
                (dataframe['macd'] > -14) &
                (dataframe['plus_di'] > dataframe['minus_di']) &
                (dataframe['adx'] > 33) &
                (dataframe["close"] > minimum_coin_price)
            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['macd'] < 0) &
                (dataframe['minus_di'] > dataframe['plus_di']) &
                (dataframe['adx'] < 26)
            ),
            'sell'] = 1
        return dataframe
