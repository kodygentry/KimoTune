# 🎧 KimoTune – Real-Time Audio Mood Visualizer

KimoTune is a real-time audio analysis tool that listens to your music and visualizes its mood using fun kaomojis. It analyzes frequency bands (bass, mids, highs), detects overall energy, and displays mood-based feedback frame-by-frame in your console.

---

## 🚀 Features

- 🎶 Real-time FFT-based audio analysis  
- 💡 Mood classification (e.g. dreamy, punchy, chaotic)  
- 😊 Kaomoji mood display  
- 🔊 Audio playback synced with analysis  
- ✅ Clean, modular Python structure

---

## 📁 Project Structure
```
KimoTune/
├── audio/ # Place your MP3 or WAV files here
│ └── crush.mp3
├── config.py # Configuration and mood mapping
├── mood_logic.py # Audio analysis and mood detection logic
├── utils.py # Console utilities (bars, clearing)
├── main.py # Main entry point
├── requirements.txt # Python dependencies
├── .gitignore
└── README.md # You're reading it!
```
---

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/KimoTune.git
   cd KimoTune
   ```
   
Install dependencies:
pip install -r requirements.txt

Add your audio file:
Place your.mp3 inside the audio folder.

▶️ Run the Program
python main.py
You'll see real-time playback with mood-based visual feedback like:
```
🎧  Time: 3.2s | Mood: dreamy (｡•́‿•̀｡)

- Bass:   ████████████               0.421
- Mids:   ███████████████████        0.693
- Highs:  ██████                     0.202
- Energy: ██████████████            0.513
```

📄 License
MIT License – do what you want, just don't remove the credits!

❤️ Credits
Built with Python, librosa, sounddevice
By [Kody Gentry].
