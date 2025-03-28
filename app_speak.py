import streamlit as st
import pandas as pd
import speech_recognition as sr
import os

# 📌 문제 데이터 (예제)
df = pd.DataFrame({
    "Korean": ["안녕하세요", "고맙습니다", "사랑해요"],
    "English": ["Hello", "Thank you", "I love you"]
})

# 📌 세션 상태 초기화
if "last_quiz" not in st.session_state:
    st.session_state.last_quiz = None
    st.session_state.last_answer = None

# 🎯 퀴즈 문제 설정 (새로고침 방지)
if st.session_state.last_quiz is None:
    df_sample = df.sample(n=1, random_state=42)  # 🔥 랜덤 but 고정된 값 유지
    st.session_state.last_quiz = df_sample.iloc[0]["Korean"]
    st.session_state.last_answer = df_sample.iloc[0]["English"]

df_quiz = pd.DataFrame({"Quiz": [st.session_state.last_quiz]})
df_answer = pd.DataFrame({"Answer": [st.session_state.last_answer]})

# 📝 테이블 표시 (고정)
st.table(df_quiz)
st.table(df_answer)

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
