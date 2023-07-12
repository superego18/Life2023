#!/usr/bin/env python
# coding: utf-8

# # 필요한 패키지 다운로드

# In[1]:


import pandas as pd
import numpy as np

from scipy.stats.mstats import winsorize

from datetime import datetime
import pandas_market_calendars as mcal


# # 데이터셋 전처리

# In[86]:


class preprocessing:
    def __init__(self, df):
        self.df = df
        self.index_to_datetime()
        self.make_log_chg_pct_1d()
        self.cut_with_valid_date()
        self.fill_na()
        self.winsorizing()
        
    def index_to_datetime(self):
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df.set_index('date', inplace=True)
        
    def make_log_chg_pct_1d(self):
        self.df['LOG_CHG_PCT_1D'] = np.log(self.df['CHG_PCT_1D']/100 + 1)
    
    def cut_with_valid_date(self):
        first_valid_date = np.where(~np.isnan(self.df.to_numpy()).any(axis=1))[0][0]
        self.df = self.df.iloc[first_valid_date:]
        
    def get_na_days_list(self, market1, market2, start_date, end_date):

        krx_trading_day = market1.schedule(start_date=start_date, end_date=end_date).index.tolist()
        nyse_trading_day = market2.schedule(start_date=start_date, end_date=end_date).index.tolist()

        null_days_list = sorted(set(krx_trading_day + nyse_trading_day) - set(self.df.index))

        return null_days_list
    
    def fill_na_by_column(self):
        columns_ffill = ['PX_LAST']
        columns_zero_fill = ['CHG_PCT_1D', 'LOG_CHG_PCT_1D']

        for column in columns_ffill:
            self.df[column] = self.df[column].fillna(method='ffill')

        for column in columns_zero_fill:
            self.df[column] = self.df[column].fillna(0)

    def fill_na(self):
        krx = mcal.get_calendar('XKRX')
        nyse = mcal.get_calendar('NYSE')
        
        index_to_fill = self.get_na_days_list(krx, nyse, self.df.index[0], self.df.index[-1]) 
        self.df = self.df.reindex(self.df.index.union(index_to_fill))
        self.fill_na_by_column()
        
    def winsorizing(self):
        self.df['LOG_CHG_PCT_1D_win'] = winsorize(self.df['LOG_CHG_PCT_1D'], limits=(0.05, 0.05))

