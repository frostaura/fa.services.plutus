from functools import reduce
from typing import Any, Callable, Dict, List
import numpy as np
import pandas as pd
from pandas import DataFrame
from skopt.space import Categorical, Dimension, Integer, Real
from freqtrade.optimize.hyperopt_interface import IHyperOpt
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

class FrostAuraM8HyperOpt(IHyperOpt):
    @staticmethod
    def populate_indicators(dataframe: DataFrame, metadata: dict) -> DataFrame:
        # RSI
        dataframe['rsi'] = ta.RSI(dataframe)
        dataframe['sell-rsi'] = ta.RSI(dataframe)
        
        return dataframe
    
    @staticmethod
    def stoploss_space() -> List[Dimension]:
        return [
            Real(-0.5, -0.02, name='stoploss'),
        ]

    @staticmethod
    def buy_strategy_generator(params: Dict[str, Any]) -> Callable:
        def populate_buy_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            conditions = []
            minimum_coin_price = 0.0000015

            conditions.append(dataframe['rsi'] > params['var_rsi'])
            conditions.append(dataframe["close"] > minimum_coin_price)

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'buy'] = 1

            return dataframe

        return populate_buy_trend

    @staticmethod
    def indicator_space() -> List[Dimension]:
        return [
            Integer(60, 95, name='var_rsi')
        ]

    @staticmethod
    def sell_strategy_generator(params: Dict[str, Any]) -> Callable:
        def populate_sell_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            conditions = []
            
            previous_close = dataframe['close'].shift(1)
            current_close = dataframe['close']
            percentage_price_delta = ((previous_close - current_close) / previous_close) * -100

            rsi_condition = dataframe['sell-rsi'] < params['var_sell_rsi']
            percentage_condition = percentage_price_delta > params['var_sell_percentage']
            
            conditions.append(rsi_condition | percentage_condition)

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'sell'] = 1

            return dataframe

        return populate_sell_trend

    @staticmethod
    def sell_indicator_space() -> List[Dimension]:
        return [
            Integer(25, 60, name='var_sell_rsi'),
            Integer(1, 45, name='var_sell_percentage'),
        ]