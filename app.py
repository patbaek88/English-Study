import streamlit as st
import pandas as pd

# review 데이터 불러오기
df = pd.read_csv('review.csv')

# 10개의 무작위 샘플 추출
df_samples = df.sample(n=20)

st.title('English Quiz')  # 타이틀명 지정
st.write("")
st.write(df_samples)
st.write("")


if st.button("Reload"):
  st.experimental_rerun()

st.write("")
st.write('Review')
st.write(df)
