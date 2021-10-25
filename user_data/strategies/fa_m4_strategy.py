from pandas import DataFrame
from freqtrade.strategy import (IntParameter, IStrategy, CategoricalParameter)
import talib.abstract as ta

class FrostAuraM4Strategy(IStrategy):
    """
    This is FrostAura's mark 4 stretagy with RSI and MACD.
    
    Last Optimization:
        Profit %        : 7.07%
        Optimized for   : Last 45 days, 4h
        Avg             : 5d 18h 30m
    """
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 2

    # Minimal ROI designed for the strategy.
    minimal_roi = {
        "0": 0.578,
        "1617": 0.167,
        "2673": 0.105,
        "6903": 0
    }

    # Optimal stoploss designed for the strategy.
    stoploss = -0.307

    # Trailing stop:
    trailing_stop = False  # value loaded from strategy
    trailing_stop_positive = None  # value loaded from strategy
    trailing_stop_positive_offset = 0.0  # value loaded from strategy
    trailing_only_offset_is_reached = False  # value loaded from strategy

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
        
        # MACD
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']

        return dataframe

    buy_rsi = IntParameter([20, 80], default=24, space='buy')
    buy_rsi_direction = CategoricalParameter(['<', '>'], default='>', space='buy')
    buy_macd_direction = CategoricalParameter(['<', '>'], default='<', space='buy')

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        minimum_coin_price = 0.0000015
        
        dataframe.loc[
            (
                (dataframe['rsi'] < self.buy_rsi.value if self.buy_rsi_direction.value == '<' else dataframe['rsi'] > self.buy_rsi.value) &
                (dataframe['macd'] > dataframe['macdsignal'] if self.buy_macd_direction.value == '<' else dataframe['macd'] < dataframe['macdsignal']) &
                (dataframe["close"] > minimum_coin_price)
            ),
            'buy'] = 1

        return dataframe

    sell_rsi = IntParameter([20, 80], default=57, space='sell')
    sell_rsi_direction = CategoricalParameter(['<', '>'], default='<', space='sell')
    sell_macd_direction = CategoricalParameter(['<', '>'], default='>', space='sell')

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['rsi'] < self.sell_rsi.value if self.sell_rsi_direction.value == '<' else dataframe['rsi'] > self.sell_rsi.value) &
                (dataframe['macd'] > dataframe['macdsignal'] if self.sell_macd_direction.value == '<' else dataframe['macd'] < dataframe['macdsignal'])
            ),
            'sell'] = 1
        
        return dataframe