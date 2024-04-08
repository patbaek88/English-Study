import streamlit as st
import pandas as pd

if 'count' not in st.session_state:
    st.session_state.count = 0

increment = st.button('Increment')
if increment:
    st.session_state.count += 1

# review 데이터 불러오기
df = pd.read_csv('review.csv')

# n개의 무작위 샘플 추출
df_samples = df.sample(n=1)
df_quiz = df_samples.loc[:, ['Korean']]
df_answer = df_samples.loc[:, ['English']]

st.title('English Quiz')  # 타이틀명 지정
st.write("")
st.write(df_quiz)

if st.button("Answer"):
  st.write("df_answer")



#if st.button("Reload"):
#  st.write("")

st.write("")
st.write("")
st.write('All Sentences for the Quiz')
st.write(df)
