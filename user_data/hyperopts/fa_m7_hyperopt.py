from functools import reduce
from typing import Any, Callable, Dict, List
import numpy as np
import pandas as pd
from pandas import DataFrame
from skopt.space import Categorical, Dimension, Integer, Real
from freqtrade.optimize.hyperopt_interface import IHyperOpt
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

class FrostAuraM7HyperOpt(IHyperOpt):
    @staticmethod
    def populate_indicators(dataframe: DataFrame, metadata: dict) -> DataFrame:
        # ADX
        dataframe['adx'] = ta.ADX(dataframe)

        # MACD
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        
        # RSI
        dataframe['rsi'] = ta.RSI(dataframe)
        
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

            conditions.append(dataframe['macd'] > params['macd-value'])
            conditions.append(dataframe['adx'] > params['adx-value'])
            conditions.append(dataframe['rsi'] > params['rsi-value'])
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
            Integer(20, 80, name='rsi-value'),
            Integer(-20, 20, name='macd-value'),
            Integer(0, 50, name='adx-value')
        ]

    @staticmethod
    def sell_strategy_generator(params: Dict[str, Any]) -> Callable:
        def populate_sell_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            conditions = []

            conditions.append(dataframe['adx'] < params['sell-adx-value'])
            conditions.append(dataframe['rsi'] < params['sell-rsi-value'])
            conditions.append(dataframe['macd'] < params['sell-macd-value'])

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'sell'] = 1

            return dataframe

        return populate_sell_trend

    @staticmethod
    def sell_indicator_space() -> List[Dimension]:
        return [
            Integer(20, 80, name='sell-rsi-value'),
            Integer(-20, 20, name='sell-macd-value'),
            Integer(0, 50, name='sell-adx-value')
        ]