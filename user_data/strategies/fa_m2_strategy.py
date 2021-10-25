from pandas import DataFrame
from freqtrade.strategy import (IntParameter, IStrategy)
import talib.abstract as ta

class FrostAuraM2Strategy(IStrategy):
    """
    This is FrostAura's mark 2 strategy which aims to make purchase decisions
    based on the Stochastic and RSI.
    
    Last Optimization:
        Profit %        : 2.32%
        Optimized for   : Last 45 days, 1h
        Avg             : 5h 23m
    """
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 2

    # Minimal ROI designed for the strategy.
    minimal_roi = {
        "0": 0.52,
        "120": 0.167,
        "723": 0.044,
        "1967": 0
    }

    # Optimal stoploss designed for the strategy.
    stoploss = -0.048

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

        return dataframe

    buy_rsi = IntParameter([15, 80], default=80, space='buy')
    buy_slowd = IntParameter([15, 45], default=42, space='buy')
    buy_slowk = IntParameter([15, 45], default=30, space='buy')

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        minimum_coin_price = 0.0000015
        
        dataframe.loc[
            (
                (dataframe['rsi'] > self.buy_rsi.value) &
                (dataframe["slowd"] > self.buy_slowd.value) &
                (dataframe["slowk"] > self.buy_slowk.value) &
                (dataframe["close"] > minimum_coin_price)
            ),
            'buy'] = 1

        return dataframe

    sell_rsi = IntParameter([20, 80], default=76, space='sell')
    sell_slowd = IntParameter([45, 80], default=48, space='sell')
    sell_slowk = IntParameter([45, 80], default=58, space='sell')

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['rsi'] < self.sell_rsi.value) &
                (dataframe["slowd"] < self.sell_slowd.value) &
                (dataframe["slowk"] < self.sell_slowk.value)
            ),
            'sell'] = 1
        
        return dataframe