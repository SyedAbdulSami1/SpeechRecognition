import streamlit as st
import os
import tempfile
from pydub import AudioSegment
import speech_recognition as sr

st.set_page_config(page_title="اردو وائس میسج ٹو ٹیکسٹ", layout="centered")
st.title("📢 WhatsApp وائس میسج اردو میں ٹیکسٹ میں تبدیل کریں")

uploaded_file = st.file_uploader("🔊 اپنی WhatsApp آڈیو فائل (.ogg یا .opus) اپلوڈ کریں", type=["ogg", "opus"])

if uploaded_file:
    recognizer = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as temp_audio:
        temp_audio.write(uploaded_file.read())
        temp_audio_path = temp_audio.name

    # Convert OGG/OPUS to WAV
    audio = AudioSegment.from_file(temp_audio_path)
    wav_path = temp_audio_path.replace(".ogg", ".wav").replace(".opus", ".wav")
    audio.export(wav_path, format="wav")

    # Recognize Speech
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="ur-PK")
            st.success("🎉 آڈیو کامیابی سے ٹیکسٹ میں بدل گئی!")
            st.text_area("📝 اردو ٹیکسٹ:", value=text, height=200)
            
            # Downloadable text file
            st.download_button(
                label="📥 اردو ٹیکسٹ ڈاؤنلوڈ کریں",
                data=text,
                file_name="urdu_transcript.txt",
                mime="text/plain"
            )
        except sr.UnknownValueError:
            st.error("⚠️ معذرت، آواز کو سمجھنے میں ناکامی ہوئی۔")
        except sr.RequestError as e:
            st.error(f"❌ API سے جواب نہیں آیا: {e}")

    # Clean up
    os.remove(temp_audio_path)
    os.remove(wav_path)
