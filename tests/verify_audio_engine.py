from gtts import gTTS
import os

try:
    print("Testing gTTS...")
    text = "Audio verification successful."
    tts = gTTS(text=text, lang='en')
    filename = "verification_audio.mp3"
    tts.save(filename)
    
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        print(f"SUCCESS: {filename} created. Size: {os.path.getsize(filename)} bytes.")
    else:
        print("FAILURE: File not created or empty.")
        
except Exception as e:
    print(f"FAILURE: Exception occurred - {e}")
