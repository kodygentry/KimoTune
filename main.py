import librosa
import sounddevice as sd
import soundfile as sf
import json
import time
import threading

from config import AUDIO_PATH, FRAME_DURATION
from mood_logic import get_frame_mood
from utils import bar, clear_console

print("🎵 Loading audio...")
y, sr = librosa.load(AUDIO_PATH, sr=None, mono=True)
frame_size = int(sr * FRAME_DURATION)
total_frames = len(y) // frame_size
print(f"✅ Loaded {len(y)} samples at {sr} Hz ({total_frames * FRAME_DURATION:.1f}s total)")

def play_audio():
    print("🔊 Starting playback...")
    data, fs = sf.read(AUDIO_PATH, dtype='float32')
    sd.play(data, fs)
    sd.wait()
    print("🛑 Playback finished.")

threading.Thread(target=play_audio, daemon=True).start()

print("📊 Beginning real-time analysis...")
for i in range(total_frames):
    frame = y[i * frame_size: (i + 1) * frame_size]
    result = get_frame_mood(frame, sr)

    with open("audio_analysis.json", "w") as f:
        json.dump(result, f)

    clear_console()
    print(f"🎧  Time: {i * FRAME_DURATION:.1f}s | Mood: {result['mood']} {result['kaomoji']}")
    print()
    print(f"Bass:   {bar(result['bass'])} {result['bass']:.3f}")
    print(f"Mids:   {bar(result['mids'])} {result['mids']:.3f}")
    print(f"Highs:  {bar(result['highs'])} {result['highs']:.3f}")
    print(f"Energy: {bar(result['energy'])} {result['energy']:.3f}")

    time.sleep(FRAME_DURATION)

print("✅ Done analyzing.")
