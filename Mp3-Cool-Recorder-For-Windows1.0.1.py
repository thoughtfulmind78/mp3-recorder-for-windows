import pyaudio
import wave
import keyboard
import os
import threading
import time

def record_audio():
    global recording, frames
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 2
    fs = 44100
    filename = os.path.join(os.path.expanduser("~"), "Desktop", "audio.mp3")

    p = pyaudio.PyAudio()

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []

    print("Recording...")

    while recording:
        data = stream.read(chunk)
        frames.append(data)

    print("Recording stopped.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"Audio saved to {filename}")

def start_recording():
    global recording, record_thread, frames
    if not recording:
        recording = True
        frames = []
        record_thread = threading.Thread(target=record_audio)
        record_thread.start()

def stop_recording():
    global recording
    if recording:
        recording = False
        if record_thread and record_thread.is_alive():
            record_thread.join()

recording = False
record_thread = None
frames = []

print("MP3 Cool Recorder for Windows is running. Press Ctrl+Shift+R to start recording and Ctrl+Shift+Alt+S to stop.")

keyboard.add_hotkey("ctrl+shift+r", start_recording)
keyboard.add_hotkey("ctrl+shift+alt+s", stop_recording)

try:
    keyboard.wait()  # Keep the script running until a keyboard interrupt (Ctrl+C)
except KeyboardInterrupt:
    print("\nMP3 Cool Recorder for Windows stopped.")

if recording:
    recording = False
    if record_thread and record_thread.is_alive():
        record_thread.join()