import streamlit as st
import pandas as pd

if 'final_dataframe' not in st.session_state:   # session state 에 final 이라는 값이 없으면, 
   st.session_state['final_dataframe']= df
   # 초기 값 설정 : session_state에 final_dataframe키 값에 초기값 데이터를 집어넣습니다 .

# #아래 코드는 df의 테이블 값이 바뀌더라도 interactive하게 연동되서 바뀌지 않습니다
# st.table(df)

# #  아래 코드는  이제 dataframe가 조작될 때 마다 session_state객체 안에 final_dataframe값을 변경하면, 
# #  수정 될 때  계속 바뀌어서 보여줍니다. 
# st.table(st.session_state.final_dataframe)

# review 데이터 불러오기
df = pd.read_csv('review.csv')

# n개의 무작위 샘플 추출
df_samples = df.sample(n=1)
df_quiz = df_samples.loc[:, ['Korean']]
df_answer = df_samples.loc[:, ['English']]

st.title('English Quiz')  # 타이틀명 지정
st.write("")
#st.write(df_quiz)

if st.button("Answer"):
  st.write(df_answer)

tab1, tab2= st.tabs(['Korean' , 'English'])

with tab1:
  #tab A 를 누르면 표시될 내용
  st.write(df_quiz)
    
with tab2:
  #tab B를 누르면 표시될 내용 
  st.write(df_answer)

if st.button("Reload"):
  st.write("")

st.write("")
st.write("")
st.write('All Sentences for the Quiz')
st.write(df)
