from pandas import DataFrame
from freqtrade.strategy import (IntParameter, IStrategy, CategoricalParameter)
import talib.abstract as ta

class FrostAuraM7Strategy(IStrategy):
    """
    This is FrostAura's mark 7 strategy which aims to make purchase decisions
    based on the ADX, RSI and MACD indicators. A momentum-based strategy.
    
    Last Optimization:
        Profit %        : 6.08%
        Optimized for   : Last 45 days, 1h
        Avg             : 1d 10h 4m
    """
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 2

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi".
    minimal_roi = {
        "0": 0.409,
        "475": 0.143,
        "770": 0.066,
        "1057": 0
    }

    # Stoploss:
    stoploss = -0.312

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

        # MACD
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        
        # RSI
        dataframe['rsi'] = ta.RSI(dataframe)

        return dataframe

    buy_macd = IntParameter([-20, 20], default=-19, space='buy')
    buy_adx = IntParameter([0, 50], default=50, space='buy')
    buy_rsi = IntParameter([20, 80], default=47, space='buy')

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        minimum_coin_price = 0.0000015
        
        dataframe.loc[
            (
                (dataframe['macd'] > self.buy_macd.value) &
                (dataframe['rsi'] > self.buy_rsi.value) &
                (dataframe['adx'] > self.buy_adx.value) &
                (dataframe["close"] > minimum_coin_price)
            ),
            'buy'] = 1

        return dataframe

    sell_macd = IntParameter([-20, 20], default=0, space='sell')
    sell_adx = IntParameter([0, 50], default=32, space='sell')
    sell_rsi = IntParameter([20, 80], default=47, space='sell')

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['macd'] < self.sell_macd.value) &
                (dataframe['rsi'] < self.sell_rsi.value) &
                (dataframe['adx'] < self.sell_adx.value)
            ),
            'sell'] = 1
        return dataframe
