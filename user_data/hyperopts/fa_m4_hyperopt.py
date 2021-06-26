from functools import reduce
from typing import Any, Callable, Dict, List
import numpy as np
import pandas as pd
from pandas import DataFrame
from skopt.space import Categorical, Dimension, Integer, Real
from freqtrade.optimize.hyperopt_interface import IHyperOpt
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

class FrostAuraM4HyperOpt(IHyperOpt):
    @staticmethod
    def populate_indicators(dataframe: DataFrame, metadata: dict) -> DataFrame:
        # RSI
        dataframe['rsi'] = ta.RSI(dataframe, window=10)
        
        # MACD
        macd = ta.MACD(dataframe, window_fast=8, window_slow=21, window_sign=5)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']
        
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
            
            conditions.append(dataframe['rsi'] < params['rsi-value'])
                    
            if 'macd-direction' in params:
                if params['macd-direction'] == '>':
                    conditions.append(dataframe['macd'] > dataframe['macdsignal'])
                if params['macd-direction'] == '<':
                    conditions.append(dataframe['macd'] < dataframe['macdsignal'])

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
            Integer(10, 40, name='rsi-value'),
            Categorical(['>', '<'], name='macd-direction')
        ]

    @staticmethod
    def sell_strategy_generator(params: Dict[str, Any]) -> Callable:
        def populate_sell_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            conditions = []

            conditions.append(dataframe['rsi'] > params['sell-rsi-value'])
                    
            if 'sell-macd-direction' in params:
                if params['sell-macd-direction'] == '>':
                    conditions.append(dataframe['macd'] > dataframe['macdsignal'])
                if params['sell-macd-direction'] == '<':
                    conditions.append(dataframe['macd'] < dataframe['macdsignal'])

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'sell'] = 1

            return dataframe

        return populate_sell_trend

    @staticmethod
    def sell_indicator_space() -> List[Dimension]:
        return [
            Integer(50, 80, name='sell-rsi-value'),
            Categorical(['>', '<'], name='sell-rsi-direction'),
            Categorical(['>', '<'], name='sell-macd-direction')
        ]