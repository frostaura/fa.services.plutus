from functools import reduce
from typing import Any, Callable, Dict, List
import numpy as np
import pandas as pd
from pandas import DataFrame
from skopt.space import Categorical, Dimension, Integer, Real
from freqtrade.optimize.hyperopt_interface import IHyperOpt
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

class FrostAuraM2HyperOpt(IHyperOpt):
    @staticmethod
    def populate_indicators(dataframe: DataFrame, metadata: dict) -> DataFrame:
        # RSI
        dataframe['rsi'] = ta.RSI(dataframe)
        
        # Stochastic Slow
        stoch = ta.STOCH(dataframe)
        dataframe['slowd'] = stoch['slowd']
        dataframe['slowk'] = stoch['slowk']
        
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

            # GUARDS AND TRENDS
            conditions.append(dataframe['rsi'] > params['rsi-value'])
            conditions.append(dataframe['slowd'] > params['slowd-value'])
            conditions.append(dataframe['slowk'] > params['slowk-value'])
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
            Integer(15, 85, name='rsi-value'),
            Integer(15, 45, name='slowk-value'),
            Integer(15, 45, name='slowd-value')
        ]

    @staticmethod
    def sell_strategy_generator(params: Dict[str, Any]) -> Callable:
        def populate_sell_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            conditions = []

            # GUARDS AND TRENDS
            conditions.append(dataframe['rsi'] < params['rsi-value'])
            conditions.append(dataframe['slowd'] < params['slowd-value'])
            conditions.append(dataframe['slowk'] < params['slowk-value'])

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'sell'] = 1

            return dataframe

        return populate_sell_trend

    @staticmethod
    def sell_indicator_space() -> List[Dimension]:
        return [
            Integer(15, 85, name='rsi-value'),
            Integer(45, 85, name='slowk-value'),
            Integer(45, 85, name='slowd-value')
        ]