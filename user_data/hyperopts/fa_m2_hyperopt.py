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

            # TRIGGERS
            if 'rsi-direction' in params:
                if params['rsi-direction'] == '>':
                    conditions.append(dataframe['rsi'] > params['rsi-value'])
                if params['rsi-direction'] == '<':
                    conditions.append(dataframe['rsi'] < params['rsi-value'])
                    
            if 'slowk-direction' in params:
                if params['slowk-direction'] == '>':
                    conditions.append(dataframe['slowk'] > params['slowk-value'])
                if params['slowk-direction'] == '<':
                    conditions.append(dataframe['slowk'] < params['slowk-value'])
                    
            if 'slowd-direction' in params:
                if params['slowd-direction'] == '>':
                    conditions.append(dataframe['slowd'] > params['slowd-value'])
                if params['slowd-direction'] == '<':
                    conditions.append(dataframe['slowd'] < params['slowd-value'])
                    
            # GUARDS AND TRENDS
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
            Integer(15, 45, name='slowd-value'),
            Categorical(['>', '<'], name='rsi-direction'),
            Categorical(['>', '<'], name='slowk-direction'),
            Categorical(['>', '<'], name='slowd-direction')
        ]

    @staticmethod
    def sell_strategy_generator(params: Dict[str, Any]) -> Callable:
        def populate_sell_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            conditions = []

            # TRIGGERS
            if 'sell-rsi-direction' in params:
                if params['sell-rsi-direction'] == '>':
                    conditions.append(dataframe['rsi'] > params['sell-rsi-value'])
                if params['sell-rsi-direction'] == '<':
                    conditions.append(dataframe['rsi'] < params['sell-rsi-value'])
                    
            if 'sell-slowk-direction' in params:
                if params['sell-slowk-direction'] == '>':
                    conditions.append(dataframe['slowk'] > params['sell-slowk-value'])
                if params['sell-slowk-direction'] == '<':
                    conditions.append(dataframe['slowk'] < params['sell-slowk-value'])
                    
            if 'sell-slowd-direction' in params:
                if params['sell-slowd-direction'] == '>':
                    conditions.append(dataframe['slowd'] > params['sell-slowd-value'])
                if params['sell-slowd-direction'] == '<':
                    conditions.append(dataframe['slowd'] < params['sell-slowd-value'])
            
            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'sell'] = 1

            return dataframe

        return populate_sell_trend

    @staticmethod
    def sell_indicator_space() -> List[Dimension]:
        return [
            Integer(15, 85, name='sell-rsi-value'),
            Integer(45, 85, name='sell-slowk-value'),
            Integer(45, 85, name='sell-slowd-value'),
            Categorical(['>', '<'], name='sell-rsi-direction'),
            Categorical(['>', '<'], name='sell-slowk-direction'),
            Categorical(['>', '<'], name='sell-slowd-direction')
        ]