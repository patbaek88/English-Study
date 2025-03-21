import streamlit as st
import pandas as pd
from gtts import gTTS
import io
from io import BytesIO
import os
from pydub import AudioSegment


from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import tempfile
import ffmpeg


password_input = st.text_input("암호를 입력해주세요",type= "password")

if password_input == "cmcpl":

  
  # review 데이터 불러오기
  dataframe = pd.read_csv('review_speak.csv', encoding="euc-kr")

  topics = dataframe["Topic"].drop_duplicates().tolist()


  # Create Radio Buttons
  topic=st.radio(label = '학습 주제선택', options = topics)

    
  
  df = dataframe[dataframe['Topic'].isin(selected_topics)]




  with st.expander('선택한 학습 주제의 모든 문장 보기'):
      st.write(df)

  st.write("")
  st.subheader('English Quiz')  # 타이틀명 지정

  if 'used_samples' not in st.session_state:
    st.session_state.used_samples =[]
  if 'last_quiz' not in st.session_state:
    st.session_state.last_quiz = None
  
  # n개의 무작위 샘플 추출
  #n_quiz = st.number_input('한번에 나오는 문제 수 설정', 0, 99, value = 1)
  n_quiz =1

  #Remove already used samples
  remaining_samples = df[~df.index.isin(st.session_state.used_samples)]

  if remaining_samples.empty:
    st.write("No more new quizzes available!")
    st.session_state.used_samples = []
    st.session_state.last_quiz = None
  else:
    df_samples = remaining_samples.sample(n=n_quiz, replace=False)
    st.session_state.used_samples.append(df_samples.index[0])
    
    df_quiz = df_samples.loc[:, ['Korean']]
    df_answer = df_samples.loc[:, ['English']]
    quiz = df_quiz.iloc[0,0]
    answer = df_answer.iloc[0,0]
    
    sound_file = BytesIO()
    tts = gTTS(answer, lang='en')
    tts.write_to_fp(sound_file)
   
    tab1, tab2, tab3 = st.tabs(['Korean' , 'English', 'English Listening'])
    with tab1:
      #tab A 를 누르면 표시될 내용
      st.table(df_quiz)
      
    with tab2:
      #tab B를 누르면 표시될 내용 
      st.table(df_answer)
  
    with tab3:
      #tab C를 누르면 표시될 내용
      
      st.audio(sound_file)
    
      
  if st.button("Reload"):
    st.write("")



  
else:
  st.write("")
  
