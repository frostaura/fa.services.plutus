from pandas import DataFrame
from freqtrade.strategy.interface import IStrategy
from freqtrade.strategy import (IntParameter, IStrategy, CategoricalParameter)
import urllib.request
import json

class FrostAuraBifrostStrategy(IStrategy):
    """
    This is FrostAura's AI strategy powered by the FrostAura Bifrost API.

    Last Optimization:
        Profit %        : --.--%
        Optimized for   : Last 45 days, 1h
        Avg             : -d -h -m
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

    def __get_bifrost_prediction__(self, dataframe: DataFrame, metadata: dict) -> float:
        latest_time_entry: str = str(dataframe.date.values[-1])
        pair_name: str = metadata['pair'].replace('/', '')
        bifrost_request_url: str = f'https://bifrost.frostaura.net/api/v1/binance/pair/{pair_name}/period/{self.timeframe}/next?cutoff_time_utc={latest_time_entry}'

        print(f'Bifrost Request Url: {bifrost_request_url}')

        response_string = urllib.request.urlopen(bifrost_request_url).read()
        response_parsed = json.loads(response_string)
        latest_value = dataframe.close.values[-1]
        predicted_value = response_parsed['predicted_close']
        delta_percentage = latest_value / (predicted_value - latest_value)
        predictions = {
            'prediction': predicted_value,
            'price_predicted_to_increase': predicted_value > latest_value,
            'delta_percentage': delta_percentage,
            'latest_value': latest_value
        }
        
        print(f'Bifrost Prediction: {predictions}')
        return predictions

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return dataframe

    buy_prediction_delta_direction = CategoricalParameter(['<', '>'], default='>', space='buy')
    buy_prediction_delta = IntParameter([1, 25], default=5, space='buy')

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        bifrost_prediction = self.__get_bifrost_prediction__(dataframe=dataframe, metadata=metadata)
        prediction_delta = bifrost_prediction['delta_percentage']

        dataframe.loc[
            (
                (prediction_delta < self.buy_prediction_delta.value if self.buy_prediction_delta_direction.value == '<' else prediction_delta > self.buy_prediction_delta.value)
            ),
            'buy'] = 1

        return dataframe

    sell_prediction_delta_direction = CategoricalParameter(['<', '>'], default='>', space='sell')
    sell_prediction_delta = IntParameter([1, 25], default=5, space='sell')

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        bifrost_prediction = self.__get_bifrost_prediction__(dataframe=dataframe, metadata=metadata)
        prediction_delta = bifrost_prediction['delta_percentage']

        dataframe.loc[
            (
                (prediction_delta < self.sell_prediction_delta.value if self.sell_prediction_delta_direction.value == '<' else prediction_delta > self.sell_prediction_delta.value)
            ),
            'sell'] = 1

        return dataframe
