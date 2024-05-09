import streamlit as st
import pandas as pd
from gtts import gTTS
from io import BytesIO
import os

password_input = st.text_input("암호를 입력해주세요",type= "password")
if password_input == "cmcpl":
  # scenario 데이터 불러오기
  data = pd.read_csv('scenario.csv')
  data1 = pd.read_csv('scenario.csv')
  data1.set_index('Order', inplace=True)
  temp_audio_dir = 'temp_audio'
  os.makedirs(temp_audio_dir, exist_ok=True)

  st.title("Biweekly Conference Call Scenario")
  st.write("")
  st.write("Participants From LG Chem:")
  st.write("  Alex Park - Project Manager")
  st.write("  Jenny Lee - Regulatory Affairs Specialist")
  st.write("")
  st.write("Participants From Thermo Fisher Scientific (TFS):")
  st.write("  Dr. Robert Smith - Clinical Operations Manager")
  st.write("  Karen Davis - Quality Assurance Lead")
  st.write("  Mark Johnson - Production Supervisor")
  st.write("")
  st.write("Scenario:")


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
    #if st.button("Show Text"):
    #  st.write(f"{english_sentence}")
    st.write(f"{korean_translation}")
    st.write(f"{english_sentence}")
    st.write("")
        
  
else:
  st.write("")

