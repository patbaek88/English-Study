import streamlit as st
import pandas as pd
from gtts import gTTS
from playsound import playsound

password_input = st.text_input("암호를 입력해주세요",type= "password")

if password_input == "cmcpl":
  # review 데이터 불러오기
  df = pd.read_csv('review.csv')
  
  # n개의 무작위 샘플 추출
  df_samples = df.sample(n=1)
  df_quiz = df_samples.loc[:, ['Korean']]
  df_answer = df_samples.loc[:, ['English']]
  answer = df_answer.iloc[0,0]

  st.title('English Quiz')  # 타이틀명 지정
  st.write("")
  #st.write(df_quiz)

  #if st.button("Answer"):
  #  st.write(df_answer)

  tab1, tab2, tab3 = st.tabs(['Korean' , 'English', 'English-Audio'])
  with tab1:
    #tab A 를 누르면 표시될 내용
    st.table(df_quiz)
    
  with tab2:
    #tab B를 누르면 표시될 내용 
    st.table(df_answer)

  with tab3:
    #tab C를 누르면 표시될 내용 
    st.table(df_answer)
    audio = 'speech.mp3'
    language = 'en'
    sp = gTTS(lang= language, text = answer, slow = False)
    sp.save(audio)
    playsound(audio)

  if st.button("Reload"):
    st.write("")

  st.write("")
  st.write("")
  #st.write('All Sentences for the Quiz')
  with st.expander('Show All Sentences'):
      st.write(df)

  #st.write(df)
else:
  st.write("")


