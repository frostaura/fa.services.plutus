from pandas import DataFrame
import pandas as pd
from freqtrade.strategy.interface import IStrategy
from freqtrade.strategy import (IntParameter, IStrategy, CategoricalParameter)
import urllib.request
import json

class FrostAuraBifrostStrategy(IStrategy):
    """
    This is FrostAura's AI strategy powered by the FrostAura Bifrost API.

    Last Optimization:
        Profit %        : 29.97%
        Optimized for   : Last 45 days, 1h
        Avg             : 2d 16h 37m
    """
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 2

    # Minimal ROI designed for the strategy.
    minimal_roi = {
        "0": 0.561,
        "427": 0.182,
        "1040": 0.03,
        "2358": 0
    }

    # Optimal stoploss designed for the strategy.
    stoploss = -0.329

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

    def __get_bifrost_bulk_prediction__(self, dataframe: DataFrame, metadata: dict) -> float:
        pair_name: str = metadata['pair'].replace('/', '')
        # This API is set up via Docker Compose. View the docker-compose.yml file for more.
        bifrost_request_url: str = f'http://bifrost/api/v1/binance/pair/{pair_name}/period/{self.timeframe}/bulk/45'

        print(f'Bifrost Request Url: {bifrost_request_url}')

        response_string = urllib.request.urlopen(bifrost_request_url).read()
        response_parsed = json.loads(response_string)
        predictions = pd.DataFrame(response_parsed['data'])

        print(f'Bifrost Prediction Count: {len(predictions)} vs {len(dataframe)} true count.')

        return predictions

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        predictions = self.__get_bifrost_bulk_prediction__(dataframe, metadata)
        new_df = dataframe.tail(len(dataframe))
        new_df['delta_percentage'] = pd.to_numeric(predictions.delta_percentages)

        return new_df

    buy_prediction_delta_direction = CategoricalParameter(['<', '>'], default='>', space='buy')
    buy_prediction_delta = IntParameter([-10000000, 10000000], default=-423044, space='buy')

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        prediction_delta = dataframe['delta_percentage']

        dataframe.loc[
            (
                (prediction_delta < self.buy_prediction_delta.value if self.buy_prediction_delta_direction.value == '<' else prediction_delta > self.buy_prediction_delta.value)
            ),
            'buy'] = 1

        return dataframe

    sell_prediction_delta_direction = CategoricalParameter(['<', '>'], default='<', space='sell')
    sell_prediction_delta = IntParameter([-10000000, 10000000], default=-4136789, space='sell')

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        prediction_delta = dataframe['delta_percentage']

        dataframe.loc[
            (
                (prediction_delta < self.sell_prediction_delta.value if self.sell_prediction_delta_direction.value == '<' else prediction_delta > self.sell_prediction_delta.value)
            ),
            'sell'] = 1

        return dataframe
