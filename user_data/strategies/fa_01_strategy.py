# --- Do not remove these libs ---
from freqtrade.strategy import IStrategy
from typing import Dict, List
from functools import reduce
from pandas import DataFrame
# --------------------------------

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
from typing import Dict, List
from functools import reduce
from pandas import DataFrame, DatetimeIndex, merge
# --------------------------------

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
import numpy  # noqa

from freqtrade.strategy import (IntParameter, IStrategy, DecimalParameter)

class FrostAura01Strategy(IStrategy):
    """
    This is FrostAura's GPT 01 strategy. A reasonably safe trading strategy combining EMA crossovers and RSI. 

    Last Optimization:
        Profit %        : 10.93%
        Optimized for   : Last 30 days, 15m
        Avg             : 19h
    """  
    INTERFACE_VERSION: int = 3  
    minimal_roi = {  
        "0": 0.01  
    }  
    stoploss = -0.05  
    timeframe = '15m'  

    # Hyperopt parameters  
    rsi_period = IntParameter(2, 30, default=5, space='buy')  
    ema_rsi_period = IntParameter(2, 30, default=5, space='buy')  
    ema100_period = IntParameter(20, 200, default=50, space='buy')  
    bb_window = IntParameter(10, 50, default=20, space='buy')  
    bb_stds = DecimalParameter(1.0, 3.0, default=2.0, space='buy')  
    bb_multiplier = DecimalParameter(0.9, 1.0, default=0.985, space='buy')  
    volume_window = IntParameter(5, 50, default=30, space='buy')  
    volume_multiplier = DecimalParameter(1.0, 50.0, default=20.0, space='buy')  

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:  
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=self.rsi_period.value)  
        rsiframe = DataFrame(dataframe['rsi']).rename(columns={'rsi': 'close'})  
        dataframe['emarsi'] = ta.EMA(rsiframe, timeperiod=self.ema_rsi_period.value)  
        macd = ta.MACD(dataframe)  
        dataframe['macd'] = macd['macd']  
        dataframe['adx'] = ta.ADX(dataframe)  
        bollinger = qtpylib.bollinger_bands(  
            qtpylib.typical_price(dataframe),  
            window=self.bb_window.value,  
            stds=self.bb_stds.value  
        )  
        dataframe['bb_lowerband'] = bollinger['lower']  
        dataframe['bb_middleband'] = bollinger['mid']  
        dataframe['bb_upperband'] = bollinger['upper']  
        dataframe['ema100'] = ta.EMA(dataframe, timeperiod=self.ema100_period.value)  
        return dataframe  

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:  
        dataframe.loc[  
            (  
                (dataframe['close'] < dataframe['ema100']) &  
                (dataframe['close'] < self.bb_multiplier.value * dataframe['bb_lowerband']) &  
                (  
                    dataframe['volume'] < (  
                        dataframe['volume']  
                        .rolling(window=self.volume_window.value)  
                        .mean()  
                        .shift(1) * self.volume_multiplier.value  
                    )  
                )  
            ),  
            'enter_long'] = 1  
        return dataframe  

    sell_multiplier = DecimalParameter(0.1, 1.9, default=1.0, space='sell')  

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:  
        dataframe.loc[  
            (  
                (dataframe['close'] > (dataframe['bb_middleband'] * self.sell_multiplier.value))  
            ),  
            'exit_long'] = 1  
        return dataframe