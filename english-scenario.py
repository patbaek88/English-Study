import streamlit as st
import pandas as pd
from gtts import gTTS
from io import BytesIO
import os

password_input = st.text_input("암호를 입력해주세요",type= "password")
if password_input == "cmcpl":
  # scenario 데이터 불러오기
  data = pd.read_csv('scenario.csv')
  temp_audio_dir = 'temp_audio'
  os.makedirs(temp_audio_dir, exist_ok=True)
  

  tab1, tab2 = st.tabs(['Scenario-Audio', 'Scenario-Text'])
  with tab1:
    #tab 1을 누르면 표시될 내용
    for index, row in data.iterrows():
      english_sentence = row['English']
      korean_translation = row['Korean']
      speaker = row['Name']
      order = row['Order']
      tts=gTTS(english_sentence, lang='en')
      audio_file_path = os.path.join(temp_audio_dir, f'audio_{index}.mp3')
      tts.save(audio_file_path)
      st.write(f"{order}. {speaker}")
      st.audio(audio_file_path)
      #st.write(f"{english_sentence}")
      #st.write(f"{korean_translation}")
      st.write("")
        
  with tab2:  
    st.write(data, hide_index = True)
    

else:
  st.write("")

