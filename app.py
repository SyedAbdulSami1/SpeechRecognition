import os
import speech_recognition as sr
from pydub import AudioSegment

# آڈیو فولڈر کا راستہ
audio_folder = "voice_files"
output_folder = "transcripts"

# آؤٹ پٹ فولڈر بنائیں اگر نہ ہو
os.makedirs(output_folder, exist_ok=True)

# سپیچ ریکگنائزر انیشیالائز کریں
recognizer = sr.Recognizer()

# تمام آڈیو فائلز پر لوپ
for filename in os.listdir(audio_folder):
    if filename.endswith(".ogg") or filename.endswith(".opus"):
        filepath = os.path.join(audio_folder, filename)
        wav_path = filepath.replace(".ogg", ".wav").replace(".opus", ".wav")
        
        # کنورٹ ogg/opus to wav
        audio = AudioSegment.from_file(filepath)
        audio.export(wav_path, format="wav")

        # سپیچ ٹو ٹیکسٹ
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language="ur-PK")
                print(f"✅ {filename} → {text}")
                
                # متن کو .txt فائل میں محفوظ کریں
                text_filename = os.path.splitext(filename)[0] + ".txt"
                with open(os.path.join(output_folder, text_filename), "w", encoding="utf-8") as f:
                    f.write(text)
            except sr.UnknownValueError:
                print(f"⚠️ Could not understand {filename}")
            except sr.RequestError as e:
                print(f"❌ API error for {filename}: {e}")

        # عارضی .wav فائل ڈیلیٹ کریں
        os.remove(wav_path)
