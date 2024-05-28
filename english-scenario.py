import streamlit as st
import pandas as pd
from gtts import gTTS
from io import BytesIO
import os

password_input = st.text_input("암호를 입력해주세요",type= "password")
if password_input == "cmcpl":
  # scenario 데이터 불러오기
  filename = st.selectbox('시나리오 선택', ('scenario_8.csv', 'scenario_9.csv'))
  data = pd.read_csv(filename)
  data1 = pd.read_csv(filename)
  data1.set_index('Order', inplace=True)
  temp_audio_dir = 'temp_audio'
  os.makedirs(temp_audio_dir, exist_ok=True)
  st.header("Biweekly Conference Call Scenario")
  st.write("")
  st.subheader("Scenario:")
  st.write("Participants:")
  members = data1.groupby("Company")["Name"].unique()  
  st.write(members)

  accent = st.selectbox('Select an English accent', ( 'us', 'com.au', 'co.uk', 'ca', 'co.in', 'ie', 'co.za'))
  #lang = st.selectbox('Select an English accent', ( 'en-au', 'en-ca', 'en-gb', 'en-gh', 'en-ie', 'en-in', 'en-ng', 'en-nz', 'en-ph', 'en-tz', 'en-uk', 'en-us', 'en-za', 'en'))

  for index, row in data.iterrows():
    english_sentence = row['English']
    korean_translation = row['Korean']
    speaker = row['Name']
    order = row['Order']
    tts=gTTS(english_sentence, lang='en', tld=accent)
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

