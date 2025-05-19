import numpy as np
import time
from config import MOODS

def get_animated_kaomoji(mood, frame_index=None):
    kaos = MOODS.get(mood, MOODS["unknown"])
    if frame_index is not None:
        return kaos[frame_index % len(kaos)]
    else:
        idx = int(time.time() * 2) % len(kaos)
        return kaos[idx]

def get_frame_mood(frame, sr, frame_index=None):
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
        "kaomoji": get_animated_kaomoji(mood, frame_index)
    }
