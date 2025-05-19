import os
import librosa
import sounddevice as sd
import soundfile as sf
import numpy as np
import pygame
import threading
import time
import random

from config import FRAME_DURATION, SONG_LIST
from mood_logic import get_frame_mood, get_animated_kaomoji

# === Globals ===
song_index = 0
song_title, audio_data, sr = None, None, None
frame_size = 0
total_frames = 0
current_audio_path = None
should_restart = True
is_playing = False

# === Load song ===
def load_song(index):
    global current_audio_path
    title, path = SONG_LIST[index]
    data, sr = librosa.load(path, sr=None, mono=True)
    current_audio_path = path
    return title, data, sr

# Load the first song
song_title, audio_data, sr = load_song(song_index)
frame_size = int(sr * FRAME_DURATION)
total_frames = len(audio_data) // frame_size

# === Audio playback loop ===
def audio_loop():
    global is_playing, should_restart, current_audio_path
    while True:
        if should_restart and current_audio_path:
            should_restart = False
            sd.stop()  # stop currently playing audio immediately
            if os.path.exists(current_audio_path):
                data, fs = sf.read(current_audio_path, dtype='float32')
                sd.play(data, fs)
        time.sleep(0.1)

threading.Thread(target=audio_loop, daemon=True).start()

# === Pygame Setup ===
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🌈 Audio Mood Visualizer")
font = pygame.font.SysFont("Consolas", 28)
clock = pygame.time.Clock()

MOOD_COLORS = {
    "dreamy": (120, 160, 255),
    "chaotic": (255, 40, 40),
    "punchy": (255, 160, 40),
    "idle": (60, 60, 60),
    "bright": (255, 255, 180),
    "bouncy": (100, 255, 220),
    "nostalgic": (180, 100, 255),
    "balanced": (80, 200, 120),
    "focused": (100, 200, 255),
    "sharp": (220, 255, 255),
    "dull": (30, 30, 30),
    "unknown": (80, 80, 80)
}

def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

# === Visualizer Setup ===
BAR_COUNT = 64
bar_width = WIDTH // BAR_COUNT
current_color = MOOD_COLORS["unknown"]
target_color = current_color
color_transition_progress = 1.0
prev_mood = "unknown"

# === Main Loop ===
i = 0
while True:
    if i >= total_frames:
        i = 0
        continue

    # Handle input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                song_index = (song_index + 1) % len(SONG_LIST)
                song_title, audio_data, sr = load_song(song_index)
                frame_size = int(sr * FRAME_DURATION)
                total_frames = len(audio_data) // frame_size
                i = 0
                should_restart = True
            elif event.key == pygame.K_LEFT:
                song_index = (song_index - 1) % len(SONG_LIST)
                song_title, audio_data, sr = load_song(song_index)
                frame_size = int(sr * FRAME_DURATION)
                total_frames = len(audio_data) // frame_size
                i = 0
                should_restart = True

    # Get frame and mood
    frame = audio_data[i * frame_size:(i + 1) * frame_size]
    result = get_frame_mood(frame, sr, frame_index=i)

    # Handle mood color
    new_mood = result["mood"]
    if new_mood != prev_mood:
        prev_mood = new_mood
        target_color = MOOD_COLORS.get(new_mood, MOOD_COLORS["unknown"])
        color_transition_progress = 0.0

    if color_transition_progress < 1.0:
        color_transition_progress += 0.05
    current_color = lerp_color(current_color, target_color, color_transition_progress)

    # Background gradient
    gradient = pygame.Surface((WIDTH, HEIGHT))
    for row in range(HEIGHT):
        blend = row / HEIGHT
        col = lerp_color((0, 0, 0), current_color, blend)
        pygame.draw.line(gradient, col, (0, row), (WIDTH, row))
    screen.blit(gradient, (0, 0))

    # Frequency bars
    fft = np.abs(np.fft.fft(frame)[:frame_size // 2])
    fft = fft / np.max(fft) if np.max(fft) > 0 else fft
    step = len(fft) // BAR_COUNT
    bar_heights = [np.mean(fft[j * step:(j + 1) * step]) for j in range(BAR_COUNT)]

    for b in range(BAR_COUNT):
        bar_height = int(bar_heights[b] * HEIGHT * 0.8)
        x = b * bar_width
        y = HEIGHT - bar_height
        pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width - 2, bar_height))

    # Mood label
    mood_text = f"{new_mood.upper()}  {get_animated_kaomoji(new_mood, frame_index=i)}"
    mood_surface = font.render(mood_text, True, (255, 255, 255))
    screen.blit(mood_surface, (WIDTH // 2 - mood_surface.get_width() // 2, 20))

    # Song name
    song_surface = font.render(f"♪ {song_title}", True, (255, 255, 255))
    screen.blit(song_surface, (WIDTH // 2 - song_surface.get_width() // 2, HEIGHT - 40))

    pygame.display.flip()
    clock.tick(1 / FRAME_DURATION)
    i += 1
