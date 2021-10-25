import numpy as np
import pandas as pd
from pandas import DataFrame
from freqtrade.strategy import (IntParameter, IStrategy, CategoricalParameter)
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

class FrostAuraM3Strategy(IStrategy):
    """
    This is FrostAura's mark 3 strategy which aims to make purchase decisions
    based on the BB, RSI and Stochastic.
    
    Last Optimization:
        Profit %        : 7.04%
        Optimized for   : Last 45 days, 1h
        Avg             : 2d 5h 20m
    """
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 2

    # Minimal ROI designed for the strategy.
    minimal_roi = {
        "0": 0.186,
        "226": 0.145,
        "809": 0.085,
        "2235": 0
    }

    # Stoploss:
    stoploss = -0.303

    # Trailing stop:
    trailing_stop = False  # value loaded from strategy
    trailing_stop_positive = None  # value loaded from strategy
    trailing_stop_positive_offset = 0.0  # value loaded from strategy
    trailing_only_offset_is_reached = False  # value loaded from strategy

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

    # Number of candles the strategy requires before producing valid signals.
    startup_candle_count: int = 30

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
        # RSI
        dataframe['rsi'] = ta.RSI(dataframe)
        
        # Stochastic Slow
        stoch = ta.STOCH(dataframe)
        dataframe['slowd'] = stoch['slowd']
        dataframe['slowk'] = stoch['slowk']

        # Bollinger Bands
        bollinger1 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=1)
        dataframe['bb_lowerband1'] = bollinger1['lower']
        dataframe['bb_middleband1'] = bollinger1['mid']
        dataframe['bb_upperband1'] = bollinger1['upper']
        
        bollinger2 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lowerband2'] = bollinger2['lower']
        dataframe['bb_middleband2'] = bollinger2['mid']
        dataframe['bb_upperband2'] = bollinger2['upper']
        
        bollinger3 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=3)
        dataframe['bb_lowerband3'] = bollinger3['lower']
        dataframe['bb_middleband3'] = bollinger3['mid']
        dataframe['bb_upperband3'] = bollinger3['upper']
        
        bollinger4 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=4)
        dataframe['bb_lowerband4'] = bollinger4['lower']
        dataframe['bb_middleband4'] = bollinger4['mid']
        dataframe['bb_upperband4'] = bollinger4['upper']

        return dataframe

    buy_rsi = IntParameter([20, 80], default=20, space='buy')
    buy_band = CategoricalParameter(['lower', 'middle', 'upper'], default='lower', space='buy')
    buy_std = CategoricalParameter(['1', '2', '3', '4'], default='2', space='buy')
    buy_slowd = IntParameter([20, 80], default=23, space='buy')
    buy_slowk = IntParameter([20, 80], default=22, space='buy')

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        minimum_coin_price = 0.0000015
        var_buy_rsi = self.buy_rsi.value
        var_buy_band = self.buy_band.value
        var_buy_std = self.buy_std.value
        var_buy_band_value = dataframe['bb_' + var_buy_band + 'band' + var_buy_std]
        var_buy_slowd = self.buy_slowd.value
        var_buy_slowk = self.buy_slowk.value
        
        dataframe.loc[
            (
                (dataframe['slowd'] < var_buy_slowd) &
                (dataframe['slowk'] < var_buy_slowk) &
                (dataframe['rsi'] < var_buy_rsi) &
                (dataframe["close"] < var_buy_band_value) &
                (dataframe["close"] > minimum_coin_price)
            ),
            'buy'] = 1

        return dataframe

    sell_rsi = IntParameter([20, 80], default=77, space='sell')
    sell_band = CategoricalParameter(['lower', 'middle', 'upper'], default='lower', space='sell')
    sell_std = CategoricalParameter(['1', '2', '3', '4'], default='4', space='sell')
    sell_slowd = IntParameter([20, 80], default=30, space='sell')
    sell_slowk = IntParameter([20, 80], default=61, space='sell')

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        var_sell_rsi = self.sell_rsi.value
        var_sell_band = self.sell_band.value
        var_sell_std = self.sell_std.value
        var_sell_band_value = dataframe['bb_' + var_sell_band + 'band' + var_sell_std]
        var_sell_slowd = self.sell_slowd.value
        var_sell_slowk = self.sell_slowk.value
        
        dataframe.loc[
            (
                (dataframe['slowd'] > var_sell_slowd) &
                (dataframe['slowk'] > var_sell_slowk) &
                (dataframe['rsi'] > var_sell_rsi) &
                (dataframe["close"] < var_sell_band_value)
            ),
            'sell'] = 1
        
        return dataframe