from gtts import gTTS
from playsound import playsound
import tempfile
import os

def speak(text):
    tts = gTTS(text)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
        tts.save(fp.name)
        playsound(fp.name)
    os.remove(fp.name)

# TEST IT
speak("你好！欢迎来到中文卡片应用。")