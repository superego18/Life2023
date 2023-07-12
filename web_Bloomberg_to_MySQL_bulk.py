#!/usr/bin/env python
# coding: utf-8

# # 초기 bulk dataset 만들기 

# ### 필요한 모듈 불러오기

# In[26]:


import datetime

# 블룸버그 터미널 관련
# import pdblp

# 병렬 연산 관련
from joblib import Parallel, delayed

# 데이터셋 전처리
import web_Dataset_Preprocessing as wDP

# 데이터셋 sql 저장
import pymysql
from sqlalchemy import create_engine


# ### 블룸버그 터미널 연결

# In[ ]:


con = pdblp.BCon(debug = False, port=8194, timeout=5000)
    # Bloomberg 서비스에 연결하기 위한 BCon 객체 생성
    # debug=False는 디버그 모드를 비활성화하는 옵션, 디버그 모드를 활성화하면 더 자세한 정보를 얻을 수 있지만, 일반적으로는 비활성화하는 것이 좋음
    # port=8194는 Bloomberg 서비스에 연결하기 위한 포트 번호, 기본 포트 번호는 8194
    # timeout=5000은 연결 시도를 중지하고 예외를 발생시킬 최대 대기 시간(밀리초), 5000밀리초(5초)로 설정되어 있으므로, 연결 시도가 5초 동안 성공하지 않으면 예외가 발생

con.start()


# ### 티커 받아오기

# In[1]:


kospi_russell_members = []


# ⬇️ (차후 개선) 코스피 멤버 추가하는 코드 추가

# In[ ]:


kopsi_members_df = con.bulkref('', 'INDX_MEMBERS')
kopsi_members = rusell_members_df[['value']]
kospi_russell_members.append(list(kopsi_members))


# ⬇️ (차후 개선) 2500개에서 짤리는 거 방지하는 코드 추가

# In[ ]:


russell_members_df = con.bulkref('RAY Index', 'INDX_MEMBERS')
russell_members = rusell_members_df[['value']]
kospi_russell_members.append(list(russell_members))


# In[ ]:


kospi_russell_tickers = [x + ' Equity' for x in kospi_russell_members]


# ### 날짜 설정

# ⬇️ (차후 개선) 시작일 협의

# In[31]:


bulk_start_date = '20150101'
bulk_end_date = datetime.date.today().strftime('%Y%m%d') # ex) '20230712'


# In[35]:


last_update_df = pd.DataFrame()


# ### 블룸버그에서 데이터셋 받기, 전처리 후 MySQL에 저장 + 날짜 저장

# ⬇️ (차후 개선) bloomberg랑 병렬 연산 같이 되는지 확인 필요

# ⬇️ (차후 개선) 'VOLUME' 넣을지 협의 -> 전처리 코드도 수정 필요함

# In[ ]:


for ticker in kospi_russell_tickers:
    
    # 블룸버그에서 raw data 받아오기
    ticker_bloomgberg_df = con.bdh(ticker, ['PX_LAST', 'CHG_PCT_1D'], bulk_start_date, bulk_end_date)
    
    # 데이터셋 전처리
    ticker_preproccesing_df = wDP.preprocessing(ticker_bloomgberg_df).df
    
    # MySQL에 데이터셋 저장
    engine = create_engine('mysql+pymysql://root:life2023@127.0.0.1:3306/datasets')
    ticker_preproccesing_df.to_sql(ticker.replace("/", "_").replace(' ','_'), con=engine, if_exists='replace', index=True)
    engine.dispose()
    
    last_update_df.loc[ticker] = ticker_preprocessing_df.index[-1].strftime('%Y%m%d')

last_update_df.to_csv('dataset_last_update_date.csv')

