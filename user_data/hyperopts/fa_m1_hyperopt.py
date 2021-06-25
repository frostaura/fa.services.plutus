from functools import reduce
from typing import Any, Callable, Dict, List
import numpy as np
import pandas as pd
from pandas import DataFrame
from skopt.space import Categorical, Dimension, Integer, Real
from freqtrade.optimize.hyperopt_interface import IHyperOpt
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

class FrostAuraM1HyperOpt(IHyperOpt):
    @staticmethod
    def populate_indicators(dataframe: DataFrame, metadata: dict) -> DataFrame:
        # RSI
        dataframe['rsi'] = ta.RSI(dataframe)
        dataframe['sell-rsi'] = ta.RSI(dataframe)

        # Bollinger bands
        bollinger1 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=1)
        dataframe['bb_lowerband1'] = bollinger1['lower']
        dataframe['bb_middleband1'] = bollinger1['mid']
        dataframe['bb_upperband1'] = bollinger1['upper']
        
        bollinger2 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lowerband2'] = bollinger2['lower']
        dataframe['bb_middleband2'] = bollinger2['mid']
        dataframe['bb_upperband2'] = bollinger2['upper']
        
        bollinger3 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=3)
        dataframe['bb_lowerband3'] = bollinger3['lower']
        dataframe['bb_middleband3'] = bollinger3['mid']
        dataframe['bb_upperband3'] = bollinger3['upper']
        
        bollinger4 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=4)
        dataframe['bb_lowerband4'] = bollinger4['lower']
        dataframe['bb_middleband4'] = bollinger4['mid']
        dataframe['bb_upperband4'] = bollinger4['upper']
        
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
            buy_frame_key = 'bb_' + params['var_buy_band'] + 'band' + params['var_buy_std']

            conditions.append(dataframe['rsi'] < params['var_buy_rsi'])                  
            conditions.append(dataframe['close'] < dataframe[buy_frame_key])
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
            Integer(20, 80, name='var_buy_rsi'),
            Categorical(['lower', 'middle', 'upper'], name='var_buy_band'),
            Categorical(['1', '2', '3', '4'], name='var_buy_std')
        ]

    @staticmethod
    def sell_strategy_generator(params: Dict[str, Any]) -> Callable:
        def populate_sell_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            conditions = []
            sell_frame_key = 'bb_' + params['var_sell_band'] + 'band' + params['var_sell_std']
            
            conditions.append(dataframe['rsi'] > params['var_sell_rsi'])
            conditions.append(dataframe['close'] > dataframe[sell_frame_key])

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'sell'] = 1

            return dataframe

        return populate_sell_trend

    @staticmethod
    def sell_indicator_space() -> List[Dimension]:
        return [
            Integer(20, 80, name='var_sell_rsi'),
            Categorical(['lower', 'middle', 'upper'], name='var_sell_band'),
            Categorical(['1', '2', '3', '4'], name='var_sell_std')
        ]