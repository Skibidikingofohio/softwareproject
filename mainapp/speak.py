from gtts import gTTS
import pygame
import tempfile
import os

def speak(text):
    try:
        # Create temp audio file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts = gTTS(text=text, lang='zh')
            tts.save(fp.name)

        # Initialize and play
        pygame.mixer.init()
        pygame.mixer.music.load(fp.name)
        pygame.mixer.music.play()

        # Wait for it to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # Clean up
        os.remove(fp.name)

    except Exception as e:
        print("TTS Error:", e)



