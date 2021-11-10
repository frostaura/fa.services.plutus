from pandas import DataFrame
from freqtrade.strategy import (IntParameter, IStrategy)
from prophet import Prophet

class FrostAuraMP1Strategy(IStrategy):
    """
    This is FrostAura's implementation of the Facebook Prophet library for time series forecasting.
    
    Last Optimization:
        Profit %        : -.--%
        Optimized for   : Last 45 days, 1h
        Avg             : -m
    """
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 2

    # Minimal ROI designed for the strategy.
    minimal_roi = {
        "0": 0.797,
        "1905": 0.212,
        "3884": 0.089,
        "4825": 0
    }

    # Stoploss:
    stoploss = -0.27

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
        # Train the Prophet model on each time tick.
        df = dataframe[['time', 'close']] \
                .rename(columns={'time': 'ds', 'close': 'y'})

        self.model = Prophet(interval_width=0.95, daily_seasonality=True)
        self.model.fit(df)

        return dataframe

    def make_predictions(self, dataframe: DataFrame, n_predictions, frequency = 'H') -> DataFrame:
        # Add the predictions to the dataframe with column name 'yhat'.
        predictions = self.model.make_future_dataframe(periods=n_predictions, freq=frequency)
        forecasts = self.model.predict(predictions)['ds', 'yhat']

        return forecasts

    buy_n_predictions = IntParameter([1, 48], default=4, space='buy')
    buy_required_delta_percentage = IntParameter([1, 100], default=1, space='buy')
    1 + 1
    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        hours_to_predict_ahead = self.buy_n_predictions.value
        predictions = self.make_predictions(dataframe, n_predictions=hours_to_predict_ahead)
        mean_prediction = predictions['yhat'].mean()
        trend_is_upwards = (mean_prediction * (1 + self.buy_required_delta_percentage.value / 100 )) > dataframe['close']

        dataframe.loc[
            (
                (trend_is_upwards)
            ),
            'buy'] = 1

        return dataframe

    sell_n_predictions = IntParameter([1, 48], default=4, space='sell')
    sell_required_delta_percentage = IntParameter([1, 100], default=1, space='sell')

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        hours_to_predict_ahead = self.sell_n_predictions.value
        predictions = self.make_predictions(dataframe, n_predictions=hours_to_predict_ahead)
        mean_prediction = predictions['yhat'].mean()
        trend_is_downwards = (mean_prediction * (1 - self.sell_required_delta_percentage.value / 100 )) < dataframe['close']
        
        dataframe.loc[
            (
                (trend_is_downwards)
            ),
            'sell'] = 1
        
        return dataframe