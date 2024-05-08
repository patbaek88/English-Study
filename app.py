import streamlit as st
import pandas as pd
from gtts import gTTS
from io import BytesIO
import os

password_input = st.text_input("암호를 입력해주세요",type= "password")

if password_input == "cmcpl":
  # review 데이터 불러오기
  df = pd.read_csv('review.csv')
  
  # n개의 무작위 샘플 추출
  df_samples = df.sample(n=1)
  df_quiz = df_samples.loc[:, ['Korean']]
  df_answer = df_samples.loc[:, ['English']]
  answer = df_answer.iloc[0,0]
  sound_file = BytesIO()
  tts = gTTS(answer, lang='en')
  tts.write_to_fp(sound_file)

  # scenario 데이터 불러오기
  data = pd.read_csv('scenario.csv')
  temp_audio_dir = 'temp_audio'
  os.makedirs(temp_audio_dir, exist_ok=True)



  

  st.title('English Quiz')  # 타이틀명 지정
  st.write("")
  #st.write(df_quiz)

  #if st.button("Answer"):
  #  st.write(df_answer)

  tab1, tab2, tab3, tab4 = st.tabs(['Korean' , 'English', 'English-Audio', 'Scenario'])
  with tab1:
    #tab A 를 누르면 표시될 내용
    st.table(df_quiz)
    
  with tab2:
    #tab B를 누르면 표시될 내용 
    st.table(df_answer)

  with tab3:
    #tab C를 누르면 표시될 내용 
    st.audio(sound_file)

  with tab4:
    #tab 4를 누르면 표시될 내용
    for index, row in data.iterrows():
      english_sentence = row['English']
      korean_translation = row['Korean']
      speaker = row['Name']
      tts=gTTS(english_sentence, lang='en')
      audio_file_path = os.path.join(temp_audio_dir, f'audio_{index}.mp3')
      tts.save(audio_file_path)
      #if st.button(f"재생: {speaker}의 영어문장"):
      st.audio(audio_file_path)

      st.write(f"번역: {korean_translation}")
    
    
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


