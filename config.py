import os

# Base directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Timing and visuals
FRAME_DURATION = .1  # seconds per analysis frame

# Song list
SONG_LIST = [
    ("Instant Crush", os.path.join(BASE_DIR, "audio", "Instant_Crush.mp3")),
    ("Clair Obscure: Lumiere", os.path.join(BASE_DIR, "audio", "Clair_Obscure.mp3"))
]

# Mood → animated kaomojis
MOODS = {
    "punchy": ["( •̀ ω •́ )✧", "(ง •̀_•́)ง", "( •̀д•́)"],
    "dreamy": ["(｡•́‿•̀｡)", "(｡♥‿♥｡)", "(ᵕ≀ ̠ᵕ )"],
    "idle": ["(-_-)zzz", "(－_－) zzZ", "(￣o￣) . z Z"],
    "chaotic": ["(╯°□°）╯︵ ┻━┻", "┻━┻ ︵ヽ(`Д´)ﾉ︵﻿ ┻━┻", "ლ(ಠ益ಠლ)"],
    "sharp": ["(≖ᴗ≖✿)", "(¬‿¬)", "( ͡° ͜ʖ ͡°)"],
    "bouncy": ["(づ｡◕‿‿◕｡)づ", "ʕ•ᴥ•ʔ", "٩(｡•́‿•̀｡)۶"],
    "nostalgic": ["(´• ω •`)", "(ಥ﹏ಥ)", "(∩˃o˂∩)♡"],
    "balanced": ["(･ω･)b", "(￣ω￣)", "ヽ(´ー｀)ノ"],
    "bright": ["(☆▽☆)", "(★ω★)", "(≧◡≦)"],
    "dull": ["(._.)", "(¬_¬)", "( •︵• )"],
    "focused": ["(ง •̀_•́)ง", "(⇀‸↼‶)", "(•̀o•́)ง"],
    "unknown": ["(◎_◎;)", "(・_・ヾ", "(°ロ°) !?"]
}
