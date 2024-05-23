import streamlit as st
import pandas as pd
from gtts import gTTS
from io import BytesIO
import os
from pydub import AudioSegment

password_input = st.text_input("암호를 입력해주세요",type= "password")

if password_input == "cmcpl":
  # review 데이터 불러오기
  dataframe = pd.read_csv('review.csv')

  st.header("학습 주제선택")
  # Create Radio Buttons
  topic=st.radio(label = 'Radio buttons', options = ['모두', '직장인을 위한 영어패턴1-25', '미국 직장인이 매일 쓰는 영어 100문장', '원어민이 가장 많이 쓰는 구동사 30개', '일상 영어 회화 패턴 20개', '회사에서 지겹도록 듣게되는 영어 문장 40개'])
  if topic == '모두':
    selected_topics =  ['직장인을 위한 영어패턴1-25', '미국 직장인이 매일 쓰는 영어 100문장', '원어민이 가장 많이 쓰는 구동사 30개', '일상 영어 회화 패턴 20개', '회사에서 지겹도록 듣게되는 영어 문장 40개']
  elif topic == '직장인을 위한 영어패턴1-25':
    selected_topics = '직장인을 위한 영어패턴1-25'
  elif topic == '미국 직장인이 매일 쓰는 영어 100문장':
    selected_topics = '미국 직장인이 매일 쓰는 영어 100문장'
  elif topic == '원어민이 가장 많이 쓰는 구동사 30개':
    selected_topics = '원어민이 가장 많이 쓰는 구동사 30개'
  elif topic == '일상 영어 회화 패턴 20개':
    selected_topics = '일상 영어 회화 패턴 20개'
  elif topic == '회사에서 지겹도록 듣게되는 영어 문장 40개':
    selected_topics = '회사에서 지겹도록 듣게되는 영어 문장 40개'
  #selected_topics = st.multiselect('학습 주제 선택',  ['직장인을 위한 영어패턴1-25', '미국 직장인이 매일 쓰는 영어 100문장', '원어민이 가장 많이 쓰는 구동사 30개', '일상 영어 회화 패턴 20개', '회사에서 지겹도록 듣게되는 영어 문장 40개'],
  #  default= ['직장인을 위한 영어패턴1-25', '미국 직장인이 매일 쓰는 영어 100문장', '원어민이 가장 많이 쓰는 구동사 30개', '일상 영어 회화 패턴 20개', '회사에서 지겹도록 듣게되는 영어 문장 40개'])

  df = dataframe[dataframe['Topic'].isin(selected_topics)]
  
  # n개의 무작위 샘플 추출
  #n_quiz = st.number_input('한번에 나오는 문제 수 설정', 0, 99, value = 1)
  n_quiz =1
  df_samples = df.sample(n=n_quiz)
  df_quiz = df_samples.loc[:, ['Korean']]
  df_answer = df_samples.loc[:, ['English']]
  quiz = df_quiz.iloc[0,0]
  answer = df_answer.iloc[0,0]
  sound_file = BytesIO()
  tts = gTTS(answer, lang='en')
  tts.write_to_fp(sound_file)

  # scenario 데이터 불러오기
  #data = pd.read_csv('scenario.csv')
  #temp_audio_dir = 'temp_audio'
  #os.makedirs(temp_audio_dir, exist_ok=True)


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
    
    st.audio(sound_file)

  if st.button("Reload"):
    st.write("")

  st.write("")
  #st.write('All Sentences for the Quiz')
  with st.expander('선택한 학습 주제 모든 문장 보기'):
      st.write(df)

  st.write("")
  st.write("모든 문장 듣기")
  audio_file_all = open('combined_all.mp3', 'rb')
  st.audio(audio_file_all.read(), format='audio/mp3')

  st.write("직장인을 위한 영어패턴1-25 듣기")
  audio_file1 = open('combined1.mp3', 'rb')
  st.audio(audio_file1.read(), format='audio/mp3')

  st.write("미국 직장인이 매일 쓰는 영어 100문장 듣기")
  audio_file2 = open('combined2.mp3', 'rb')
  st.audio(audio_file2.read(), format='audio/mp3')

  st.write("원어민이 가장 많이 쓰는 구동사 30개 듣기")
  audio_file3 = open('combined3.mp3', 'rb')
  st.audio(audio_file3.read(), format='audio/mp3')

  st.write("일상 영어 회화 패턴 20개 듣기")
  audio_file4 = open('combined4.mp3', 'rb')
  st.audio(audio_file4.read(), format='audio/mp3')

  st.write("회사에서 지겹도록 듣게되는 영어 문장 40개")
  audio_file5 = open('combined5.mp3', 'rb')
  st.audio(audio_file5.read(), format='audio/mp3')
  
  #st.write(df)

  st.write("")
  st.write("")
  link1 = '[Conference Call Scenario Link](http://english-scenario.streamlit.app)'
  st.markdown(link1, unsafe_allow_html=True)

else:
  st.write("")


