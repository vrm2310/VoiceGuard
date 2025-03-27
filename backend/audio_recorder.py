# import sounddevice as sd
# import wave
# import numpy as np
# import os

# AUDIO_FOLDER = "uploads"
# os.makedirs(AUDIO_FOLDER, exist_ok=True)

# def record_audio(filename="recorded_audio.wav", duration=5, samplerate=44100):
#     """Records audio from the microphone for a given duration."""
#     print("Recording...")
#     recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
#     sd.wait()  # Wait until recording is finished
#     filepath = os.path.join(AUDIO_FOLDER, filename)

#     # Save as a WAV file
#     with wave.open(filepath, 'wb') as wf:
#         wf.setnchannels(1)
#         wf.setsampwidth(2)  # 16-bit audio
#         wf.setframerate(samplerate)
#         wf.writeframes(recording.tobytes())

#     print(f"Recording saved: {filepath}")
#     return filepath


import sounddevice as sd
import wave
import numpy as np
import os
import threading

AUDIO_FOLDER = "uploads"
os.makedirs(AUDIO_FOLDER, exist_ok=True)

recording = []
recording_active = False
samplerate = 44100
channels = 1


def callback(indata, frames, time, status):
    """ Continuously store recorded audio chunks """
    global recording
    if recording_active:
        recording.append(indata.copy())

def start_recording():
    """ Starts recording without a fixed duration """
    global recording, recording_active
    recording = []  # Clear previous recording
    recording_active = True

    # Start recording in a separate thread
    threading.Thread(target=lambda: sd.InputStream(callback=callback, channels=channels, samplerate=samplerate).start()).start()

    print("Recording started...")

def stop_recording(filename="recorded_audio.wav"):
    """ Stops recording and saves the audio file """
    global recording_active
    recording_active = False  # Stop recording

    if not recording:
        print("No recording found.")
        return None

    # Convert recorded audio to NumPy array
    audio_data = np.concatenate(recording, axis=0)

    # Save the recorded audio
    filepath = os.path.join(AUDIO_FOLDER, filename)

    with wave.open(filepath, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.astype(np.int16).tobytes())

    print(f"Recording saved: {filepath}")
    return filepath
