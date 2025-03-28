import streamlit as st
import pandas as pd
from io import BytesIO
from gtts import gTTS

# 데이터 예시 (사용자 데이터에 맞게 수정)
df = pd.DataFrame({
    'Korean': ['안녕하세요', '고맙습니다', '사랑해요'],
    'English': ['Hello', 'Thank you', 'I love you']
})

# 세션 상태 초기화
if 'used_samples' not in st.session_state:
    st.session_state.used_samples = []
if 'last_quiz' not in st.session_state:
    st.session_state.last_quiz = None

# 문제 샘플을 사용하여 퀴즈 진행
remaining_samples = df[~df.index.isin(st.session_state.used_samples)]

if remaining_samples.empty:
    st.write("No more new quizzes available!")
    st.session_state.used_samples = []  # 모든 퀴즈가 끝나면 상태 초기화
    st.session_state.last_quiz = None
else:
    df_samples = remaining_samples.sample(n=1, replace=False)
    st.session_state.used_samples.append(df_samples.index[0])

    # 퀴즈와 답 생성
    df_quiz = df_samples.loc[:, ['Korean']]
    df_answer = df_samples.loc[:, ['English']]
    quiz = df_quiz.iloc[0, 0]
    answer = df_answer.iloc[0, 0]

    # 퀴즈 표시
    st.subheader('Quiz')
    st.write(f"퀴즈: {quiz}")

    # TTS 생성
    sound_file = BytesIO()
    tts = gTTS(answer, lang='en', slow=False)
    tts.write_to_fp(sound_file)
    
    # 음성 재생
    st.audio(sound_file, format='audio/wav')

# 새로고침 방지
# 여기에 녹음 부분을 추가하고, 녹음 후 새로운 상태로 처리되도록 조치
audio_data = st.audio_input("Record the answer in English")
if audio_data is not None:
    # 여기에 녹음 후 결과 처리하는 로직 추가
    # 녹음 결과를 텍스트로 변환하고, 사용자가 맞혔는지 확인하는 로직 등
    st.write(f"Audio recorded: {audio_data}")


  
else:
  st.write("")

