import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import os
import uuid

st.set_page_config(page_title="WhatsApp Voice to Urdu Text", page_icon="🎙️")

st.title("🎙️ WhatsApp وائس نوٹ کو اردو ٹیکسٹ میں تبدیل کریں")

# 👇 Add this block before file uploader
ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg.exe")
AudioSegment.converter = ffmpeg_path

uploaded_file = st.file_uploader("WhatsApp کی .opus فائل اپلوڈ کریں", type=["opus", "ogg"])

if uploaded_file is not None:
    st.audio(uploaded_file)

    # Save uploaded file to disk
    temp_opus_path = f"temp_{uuid.uuid4()}.opus"
    with open(temp_opus_path, "wb") as f:
        f.write(uploaded_file.read())

    # Convert to WAV using ffmpeg
    temp_wav_path = temp_opus_path.replace(".opus", ".wav")
    audio = AudioSegment.from_file(temp_opus_path)
    audio.export(temp_wav_path, format="wav")

    # Recognize speech
    r = sr.Recognizer()
    with sr.AudioFile(temp_wav_path) as source:
        st.info("آواز کو پہچانا جا رہا ہے...")
        audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data, language="ur-PK")
            st.success("📄 حاصل شدہ اردو ٹیکسٹ:")
            st.write(text)
        except sr.UnknownValueError:
            st.error("معذرت! آواز سمجھ نہیں آئی۔")
        except sr.RequestError:
            st.error("Speech recognition سروس دستیاب نہیں۔")

    # Cleanup
    os.remove(temp_opus_path)
    os.remove(temp_wav_path)
