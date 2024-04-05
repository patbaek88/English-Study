#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pandas as pd
import random

# review 데이터 불러오기
df = pd.read_csv('review.csv')

# 10개의 무작위 샘플 추출
df_samples = df.sample(n=20)
print(df_samples)

#csv로 저장
#df_samples.to_csv('quiz.csv', index=False, encoding='cp949')

