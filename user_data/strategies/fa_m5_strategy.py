from pandas import DataFrame
from freqtrade.strategy import (IntParameter, IStrategy, CategoricalParameter)
import talib.abstract as ta

class FrostAuraM5Strategy(IStrategy):
    """
    This is FrostAura's mark 5 strategy which aims to make purchase decisions
    based on the ADX and RSI indicators. A momentum-based strategy.
    
    Last Optimization:
        Profit %        : 4.03%
        Optimized for   : Last 45 days, 1h
        Avg             : 1d 2h 49m
    """
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 2

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi".
    minimal_roi = {
        "0": 0.36,
        "298": 0.18,
        "731": 0.057,
        "1050": 0
    }

    stoploss = -0.271

    # Trailing stop:
    trailing_stop = False  # value loaded from strategy
    trailing_stop_positive = None  # value loaded from strategy
    trailing_stop_positive_offset = 0.0  # value loaded from strategy
    trailing_only_offset_is_reached = False  # value loaded from strategy

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

        # RSI
        dataframe['rsi'] = ta.RSI(dataframe)

        return dataframe

    buy_adx = IntParameter([0, 50], default=50, space='buy')
    buy_di_direction = CategoricalParameter(['<', '>'], default='>', space='buy')

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        minimum_coin_price = 0.0000015
        
        dataframe.loc[
            (
                (dataframe['adx'] > self.buy_adx.value) &
                (dataframe['plus_di'] > dataframe['minus_di'] if self.buy_di_direction.value == '>' else dataframe['plus_di'] < dataframe['minus_di']) &
                (dataframe["close"] > minimum_coin_price)
            ),
            'buy'] = 1

        return dataframe

    sell_rsi = IntParameter([20, 80], default=29, space='sell')
    sell_adx = IntParameter([0, 50], default=45, space='sell')

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['rsi'] < self.sell_rsi.value) &
                (dataframe['adx'] < self.sell_adx.value)
            ),
            'sell'] = 1
        return dataframe
