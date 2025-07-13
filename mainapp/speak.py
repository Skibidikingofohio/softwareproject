from gtts import gTTS
from playsound import playsound
import tempfile
import os

def speak(text):
    try:
        tts = gTTS(text=text, lang='zh')  # Mandarin voice
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            tts.save(fp.name)
            playsound(fp.name)
            os.remove(fp.name)
    except Exception as e:
        print(f"Speech error: {e}")


