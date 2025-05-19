import os
from config import BAR_WIDTH

def bar(value, max_width=BAR_WIDTH):
    blocks = int(min(value * max_width, max_width))
    return "█" * blocks + " " * (max_width - blocks)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
