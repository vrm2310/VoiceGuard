import sounddevice as sd
import wave
import numpy as np
import os

AUDIO_FOLDER = "uploads"
os.makedirs(AUDIO_FOLDER, exist_ok=True)

def record_audio(filename="recorded_audio.wav", duration=5, samplerate=44100):
    """Records audio from the microphone for a given duration."""
    print("Recording...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()  # Wait until recording is finished
    filepath = os.path.join(AUDIO_FOLDER, filename)

    # Save as a WAV file
    with wave.open(filepath, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(samplerate)
        wf.writeframes(recording.tobytes())

    print(f"Recording saved: {filepath}")
    return filepath
