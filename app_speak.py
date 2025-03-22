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

import platform


password_input = st.text_input("암호를 입력해주세요",type= "password")

if password_input == "cmcpl":

  
  # review 데이터 불러오기
  dataframe = pd.read_csv('review_speak.csv', encoding="euc-kr")

  topics = dataframe["Topic"].drop_duplicates().tolist()


  st.write("")
  st.subheader('학습')
   # 모든 주제를 기본값으로 선택
  selected_topics = st.multiselect(label="학습 주제 선택", options=topics, default=topics)
     
  
  df = dataframe[dataframe["Topic"].isin(selected_topics)]


  # 반복 재생 여부 체크박스 추가
  repeat_audio = st.checkbox("반복 재생")
    
  # 🎵 오디오 파일 생성 (MP3 → WAV 변환)
  combined_audio_mp3 = io.BytesIO()
  combined_audio_wav = io.BytesIO()

  full_text_ko = ""
  full_text_en = ""

  for _, row in df.iterrows():
      full_text_ko += row["Korean"] + ". "
      full_text_en += row["English"] + ". "

  # 🗣️ gTTS 변환 (한국어 + 영어)
  tts_ko = gTTS(text=full_text_ko, lang="ko")
  tts_en = gTTS(text=full_text_en, lang="en")

  # MP3 파일 저장
  tts_ko.write_to_fp(combined_audio_mp3)
  tts_en.write_to_fp(combined_audio_mp3)
  combined_audio_mp3.seek(0)

  # MP3 → WAV 변환 (아이폰 호환성 해결)
  audio = AudioSegment.from_file(combined_audio_mp3, format="mp3")
  audio.export(combined_audio_wav, format="wav")
  combined_audio_wav.seek(0)

  # 🎧 오디오 재생 (아이폰에서도 원활히 작동)
  st.audio(combined_audio_wav.getvalue(), format="audio/wav", loop=repeat_audio)

  # 아이폰에서 원활한 재생을 위해 다운로드 버튼 제공
  st.download_button(label="음원 다운로드", data=combined_audio.getvalue(), file_name="audio.mp3", mime="audio/mpeg")
  
  
  with st.expander('문장 보기'):
      st.write(df)

  st.write("")
  st.subheader('Quiz')  # 타이틀명 지정

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
  
