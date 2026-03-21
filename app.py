import streamlit as st
import os
import asyncio
import subprocess
import time
import requests
import whisper
from deep_translator import GoogleTranslator
import edge_tts
from dotenv import load_dotenv

# --- КОНФІГУРАЦІЯ ---
load_dotenv() 
GOOGLE_SHEET_URL = os.getenv("GOOGLE_SHEET_URL")

st.set_page_config(page_title="UA AI Dubber", layout="centered")

@st.cache_resource
def load_whisper():
    return whisper.load_model("base")

model = load_whisper()

UKRAINIAN_VOICES = {
    "Остап (Чоловічий)": "uk-UA-OstapNeural",
    "Поліна (Жіночий)": "uk-UA-PolinaNeural"
}

def safe_translate(text, target_lang='uk'):
    """Розбиває довгий текст на шматки по 2000 символів для стабільного перекладу."""
    translator = GoogleTranslator(source='auto', target=target_lang)
    chunk_size = 2000
    if len(text) <= chunk_size:
        return translator.translate(text)
    
    # Розбиваємо текст на частини
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    translated_chunks = []
    
    for chunk in chunks:
        translated_chunks.append(translator.translate(chunk))
        time.sleep(0.5) # Невелика пауза, щоб Google не банив за швидкість
    
    return " ".join(translated_chunks)

def log_to_cloud(video_url, voice_name, p_time):
    if GOOGLE_SHEET_URL:
        try:
            country_res = requests.get('https://ipapi.co/json/', timeout=3)
            country = country_res.json().get('country_name', 'Unknown')
            
            payload = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "url": video_url,
                "lang": "uk",
                "country": country,
                "time": p_time
            }
            requests.post(GOOGLE_SHEET_URL, json=payload, timeout=5)
        except:
            pass

def cleanup():
    for f in ["v_orig.mp4", "v_voice.mp3", "final_output.mp4"]:
        if os.path.exists(f):
            try: os.remove(f)
            except: pass

# --- ІНТЕРФЕЙС ---
st.title("🇺🇦 AI Video Dubber")

url = st.text_input("Посилання на відео:")
voice_choice = st.selectbox("Оберіть голос:", list(UKRAINIAN_VOICES.keys()))

if url and st.button("🚀 ПОЧАТИ ДУБЛЯЖ"):
    start_time = time.time()
    cleanup()

    try:
        with st.status("Обробка...", expanded=True) as status:
            # 1. Завантаження
            st.write("📥 Завантаження...")
            subprocess.run(["yt-dlp", "-f", "mp4", "-o", "v_orig.mp4", url], check=True)

            # 2. Whisper
            st.write("🎙 Розпізнавання...")
            result = model.transcribe("v_orig.mp4", fp16=False)
            full_text = result["text"].strip()

            # 3. Переклад (використовуємо функцію safe_translate)
            st.write("🌍 Переклад на українську...")
            translated_text = safe_translate(full_text)

            # 4. Озвучка
            st.write("🔊 Генерація мовлення...")
            selected_voice = UKRAINIAN_VOICES[voice_choice]
            asyncio.run(edge_tts.Communicate(translated_text, selected_voice).save("v_voice.mp3"))

            # 5. Монтаж
            st.write("🎬 Зведення...")
            ffmpeg_cmd = [
                'ffmpeg', '-y', '-i', 'v_orig.mp4', '-i', 'v_voice.mp3',
                '-filter_complex', '[0:a]volume=0.2[bg];[1:a]volume=2.5[v];[bg][v]amix=inputs=2:duration=first',
                '-c:v', 'copy', '-c:a', 'aac', 'final_output.mp4'
            ]
            subprocess.run(ffmpeg_cmd, check=True)

            duration = round(time.time() - start_time, 2)
            log_to_cloud(url, voice_choice, duration)
            
            status.update(label="✅ Готово!", state="complete")

        st.video("final_output.mp4")
        
    except Exception as e:
        st.error(f"Помилка: {str(e)[:100]}") # Виводимо тільки початок помилки для чистоти
        print(f"Error details: {e}")
    finally:
        # v_orig видаляємо, final_output залишаємо для стріміт
        if os.path.exists("v_orig.mp4"): os.remove("v_orig.mp4")
        if os.path.exists("v_voice.mp3"): os.remove("v_voice.mp3")
