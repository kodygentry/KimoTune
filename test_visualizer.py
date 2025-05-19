import librosa
import numpy as np
import sounddevice as sd
import json
import time
import threading
import soundfile as sf
import os

# === CONFIG ===
AUDIO_PATH = r"C:\Users\kodyg\OneDrive\Desktop\dev\crush.mp3"
FRAME_DURATION = 0.1  # seconds per analysis frame
BAR_WIDTH = 30

# === MOOD → KAOMOJI MAPPING ===
MOODS = {
    "punchy": "( •̀ ω •́ )✧",
    "dreamy": "(｡•́‿•̀｡)",
    "idle": "(-_-)zzz",
    "chaotic": "(╯°□°）╯︵ ┻━┻",
    "sharp": "(≖ᴗ≖✿)",
    "bouncy": "(づ｡◕‿‿◕｡)づ",
    "nostalgic": "(´• ω •`)",
    "balanced": "(･ω･)b",
    "bright": "(☆▽☆)",
    "dull": "(._.)",
    "focused": "(ง •̀_•́)ง",
    "unknown": "(◎_◎;)"
}

# === LOAD AUDIO ===
print("🎵 Loading audio...")
y, sr = librosa.load(AUDIO_PATH, sr=None, mono=True)
frame_size = int(sr * FRAME_DURATION)
total_frames = len(y) // frame_size
print(f"✅ Loaded {len(y)} samples at {sr} Hz ({total_frames * FRAME_DURATION:.1f}s total)")

# === AUDIO PLAYBACK ===
def play_audio():
    print("🔊 Starting playback...")
    data, fs = sf.read(AUDIO_PATH, dtype='float32')
    sd.play(data, fs)
    sd.wait()
    print("🛑 Playback finished.")

threading.Thread(target=play_audio, daemon=True).start()

# === UTILS ===
def bar(value, max_width=BAR_WIDTH):
    blocks = int(min(value * max_width, max_width))
    return "█" * blocks + " " * (max_width - blocks)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# === MOOD DETECTION LOGIC ===
def get_frame_mood(frame):
    fft = np.fft.fft(frame)
    fft = np.abs(fft[:len(fft)//2])
    freqs = np.fft.fftfreq(len(frame), 1/sr)[:len(fft)]

    bass = fft[(freqs > 20) & (freqs < 250)].mean()
    mids = fft[(freqs >= 250) & (freqs < 2000)].mean()
    highs = fft[(freqs >= 2000) & (freqs < 8000)].mean()
    energy = fft.mean()

    mood = "unknown"

    if energy < 0.02:
        mood = "idle"
    elif energy > 0.5 and highs > mids:
        mood = "sharp"
    elif energy > 0.3 and mids > highs:
        mood = "punchy"
    elif mids > bass and energy < 0.1:
        mood = "dreamy"
    elif highs > 2 * mids and energy < 0.2:
        mood = "bright"
    elif bass > highs and mids > highs:
        mood = "bouncy"
    elif mids > bass * 1.5 and energy < 0.1:
        mood = "nostalgic"
    elif 0.1 < energy < 0.3 and abs(bass - highs) < 0.05:
        mood = "balanced"
    elif highs > mids * 2 and energy > 0.7:
        mood = "chaotic"
    elif mids > 0.2 and energy > 0.4:
        mood = "focused"
    elif energy < 0.1 and highs < 0.05:
        mood = "dull"

    return {
        "bass": round(float(bass), 3),
        "mids": round(float(mids), 3),
        "highs": round(float(highs), 3),
        "energy": round(float(energy), 3),
        "mood": mood,
        "kaomoji": MOODS.get(mood, MOODS["unknown"])
    }

# === MAIN LOOP ===
print("📊 Beginning real-time analysis...")
for i in range(total_frames):
    frame = y[i * frame_size: (i + 1) * frame_size]
    result = get_frame_mood(frame)

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
