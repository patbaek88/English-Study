import streamlit as st
import pandas as pd
from gtts import gTTS
from io import BytesIO
import os

password_input = st.text_input("암호를 입력해주세요",type= "password")
if password_input == "cmcpl":

  st.header("Conference Call Scenario")
  # scenario 데이터 불러오기
  filename = st.selectbox('Select a scenario', ('scenario_9.csv', 'scenario_8.csv'))
  data = pd.read_csv(filename)
  data1 = pd.read_csv(filename)
  data1.set_index('Order', inplace=True)
  temp_audio_dir = 'temp_audio'
  os.makedirs(temp_audio_dir, exist_ok=True)
  st.write("")
  st.subheader("Scenario:")
  st.write("Participants:")
  members = data1.groupby("Company")["Name"].unique()  
  st.write(members)


  lang_df = pd.DataFrame({'Language':['English', 'Spanish', 'French', 'German', 'Italian', 'Chinese', 'Japanese', 'Korean'],  'Code':['en', 'es', 'fr', 'de', 'it', 'zh', 'ja', 'ko']})
  lang_select = st.selectbox('Select a language', lang_df['Language'])
  lang_code = lang_df[lang_df['Language'] == lang_select]['Code']
  lang = lang_code.iloc[0]
  #lang = st.selectbox('Select a language', ['en', 'es', 'fr', 'de', 'it', 'zh', 'ja', 'ko'])
  accent = 'com'
  if lang == 'en':
    accent = st.selectbox('Select an English accent', ( 'us', 'com.au', 'co.uk', 'ca', 'co.in', 'ie', 'co.za'))
 

  for index, row in data.iterrows():
    english_sentence = row['English']
    korean_translation = row['Korean']
    speaker = row['Name']
    order = row['Order']
    tts=gTTS(english_sentence, lang=lang, tld=accent)
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

