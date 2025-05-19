import os

# Automatically get the directory where the current script lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build a path relative to that directory
AUDIO_PATH = os.path.join(BASE_DIR, "audio", "crush.mp3")

FRAME_DURATION = 0.1  # seconds per analysis frame
BAR_WIDTH = 30

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
