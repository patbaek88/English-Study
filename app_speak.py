import streamlit as st
import pandas as pd
from gtts import gTTS
import io
from io import BytesIO
import speech_recognition as sr
from pydub import AudioSegment


password_input = st.text_input("암호를 입력해주세요",type= "password")

if password_input == "cmcpl":

  
  # review 데이터 불러오기
  dataframe = pd.read_csv('review_speak.csv') #encoding="euc-kr")

  topics = dataframe["Topic"].drop_duplicates().tolist()


  st.write("")
  st.subheader('학습')
   # 모든 주제를 기본값으로 선택
  selected_topics = st.multiselect(label="학습 주제 선택", options=topics, default=None)

  accent = 'com'
  accent_df = pd.DataFrame({'Accent':['United States', 'United Kingdom', 'Ireland', 'Canada', 'Australia', 'India', 'South Africa'],  'Accent_Code':['com', 'co.uk', 'ie', 'ca', 'com.au', 'co.in', 'co.za']})
  accent_select = st.selectbox('영어 억양 선택', accent_df['Accent'])
  accent_code = accent_df[accent_df['Accent'] == accent_select]['Accent_Code']
  accent = accent_code.iloc[0]

  slow = st.checkbox("영어 읽기 느리게")

  df = dataframe[dataframe["Topic"].isin(selected_topics)]

  if st.button("음원 생성"):

    
    
    # 반복 재생 여부 체크박스 추가
    #repeat_audio = st.checkbox("반복 재생")
      
     # 음성 파일을 저장할 메모리 버퍼 생성
    audio_bytes = io.BytesIO()
    
    combined_audio = io.BytesIO()
  
    for _, row in df.iterrows():
        # 한국어 문장 변환
        tts_ko = gTTS(text=row["Korean"], lang="ko")
        tts_ko.write_to_fp(combined_audio)
  
        # 영어 문장 변환
        tts_en = gTTS(text=row["English"], lang="en", tld=accent, slow=slow)
        tts_en.write_to_fp(combined_audio)

  
    # Streamlit에서 오디오 재생
    st.audio(combined_audio.getvalue(), format="audio/mp3")
  
    # 아이폰에서 원활한 재생을 위해 다운로드 버튼 제공
    st.download_button(label="음원 다운로드", data=combined_audio.getvalue(), file_name="audio.mp3", mime="audio/mpeg")
  
  
  with st.expander('표현 보기'):
      st.write(df)

  st.write("")
  st.subheader('Quiz')  # 타이틀명 지정

  if 'used_samples' not in st.session_state:
    st.session_state.used_samples =[]
  if 'last_quiz' not in st.session_state:
    st.session_state.last_quiz = None
  

  #Remove already used samples
  remaining_samples = df[~df.index.isin(st.session_state.used_samples)]

  if remaining_samples.empty:
    st.write("No more new quizzes available!")
    st.session_state.used_samples = []
    st.session_state.last_quiz = None
  else:
    df_samples = remaining_samples.sample(n=1, replace=False, random_state=42)
    st.session_state.used_samples.append(df_samples.index[0])
    
  df_quiz = df_samples.loc[:, ['Korean']]
  df_answer = df_samples.loc[:, ['English']]
  quiz = df_quiz.iloc[0,0]
  answer = df_answer.iloc[0,0]
  
  sound_file = BytesIO()
  tts = gTTS(answer, lang='en', tld=accent, slow = slow)
  tts.write_to_fp(sound_file)
 
  tab1, tab2, tab3, tab4 = st.tabs(['Korean' , 'English', 'Listening', 'Speaking'])
  
  with tab1:
    #tab 1 를 누르면 표시될 내용
    st.table(df_quiz)
  
  with tab2:
    #tab 2를 누르면 표시될 내용 
    st.table(df_answer)

  with tab3:
    #tab 3를 누르면 표시될 내용
    autoplay = st.checkbox("자동재생")
    
    st.audio(sound_file, autoplay=autoplay)

  with tab4:
    #tab 4 를 누르면 표시될 내용
    st.table(df_quiz)

    # 🎙 음성 녹음 (새로고침 방지)
    audio_data = st.audio_input("Record English sentences")
    
    if "recorded_text" not in st.session_state:
        st.session_state.recorded_text = None
    
    if audio_data is not None:
        audio_path = "uploaded_audio.wav"
        
        with open(audio_path, "wb") as f:
            f.write(audio_data.getvalue())
    
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
    
        try:
            st.session_state.recorded_text = recognizer.recognize_google(audio, language="en")
        except sr.UnknownValueError:
            st.session_state.recorded_text = "음성을 인식할 수 없습니다."
        except sr.RequestError as e:
            st.session_state.recorded_text = f"음성 인식 서비스 오류: {e}"
    
    # 🎤 녹음된 텍스트 유지
    if st.session_state.recorded_text:
        st.write(f"🎙 인식된 문장: {st.session_state.recorded_text}")
   
      
  if st.button("Reload"):
    st.write("")



  
else:
  st.write("")
