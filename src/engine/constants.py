#!/usr/bin/env python3
"""Game Constants Configuration"""

import pygame

# Display settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TARGET_FPS = 60
FRAME_TIME = 1.0 / FPS

# Colors (default theme)
COLORS = {
    'background': '#faf8ef',
    'grid': '#bbada0',
    'empty': '#cdc1b4',
    'text_light': '#f9f6f2',
    'text_dark': '#776e65',
    'tile_2': '#eee4da',
    'tile_4': '#ede0c8',
    'tile_8': '#f2b179',
    'tile_16': '#f59563',
    'tile_32': '#f67c5f',
    'tile_64': '#f65e3b',
    'tile_128': '#edcf72',
    'tile_256': '#edcc61',
    'tile_512': '#edc850',
    'tile_1024': '#edc53f',
    'tile_2048': '#edc22e',
    'tile_super': '#3c3a32',
    'button': '#8f7a66',
    'button_hover': '#9f8b77',
    'button_pressed': '#7f6b5c',
    'accent': '#8f7a66',
    'success': '#2ecc71',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'info': '#3498db'
}

# Grid settings
GRID_SIZE = 4
TILE_SIZE = 106
TILE_PADDING = 15
GRID_OFFSET_X = (SCREEN_WIDTH - (TILE_SIZE * GRID_SIZE + TILE_PADDING * (GRID_SIZE + 1))) // 2
GRID_OFFSET_Y = 120

# Animation settings
ANIMATION_DURATION = 150
MOVE_ANIMATION_DURATION = 100
MERGE_ANIMATION_DURATION = 150
POP_ANIMATION_DURATION = 200

# Particle settings
PARTICLE_COUNT = 50
PARTICLE_LIFETIME = 1.0
PARTICLE_SPEED = 200
PARTICLE_SIZE = 3

# Sound settings
SOUND_VOLUME = 0.5
MUSIC_VOLUME = 0.3
AUDIO_CHANNELS = 8

# Difficulty settings
DIFFICULTY_LEVELS = 4
DIFFICULTY_THRESHOLD = 5  # Increase difficulty every 5 levels

# Game settings
MAX_LEVEL = 20
WIN_TILE = 1024
TILE_VALUES = {
    2: (COLORS['tile_2'], COLORS['text_dark']),
    4: (COLORS['tile_4'], COLORS['text_dark']),
    8: (COLORS['tile_8'], COLORS['text_light']),
    16: (COLORS['tile_16'], COLORS['text_light']),
    32: (COLORS['tile_32'], COLORS['text_light']),
    64: (COLORS['tile_64'], COLORS['text_light']),
    128: (COLORS['tile_128'], COLORS['text_light']),
    256: (COLORS['tile_256'], COLORS['text_light']),
    512: (COLORS['tile_512'], COLORS['text_light']),
    1024: (COLORS['tile_1024'], COLORS['text_light']),
    2048: (COLORS['tile_2048'], COLORS['text_light']),
}

# Font sizes
FONT_SIZES = {
    'title': 80,
    'heading': 48,
    'subtitle': 36,
    'large': 32,
    'medium': 28,
    'normal': 24,
    'small': 18,
    'tiny': 14
}

# Paths
ASSETS_PATH = 'assets'
FONTS_PATH = 'assets/fonts'
SOUNDS_PATH = 'assets/sounds'
IMAGES_PATH = 'assets/images'
SAVES_PATH = 'saves'
THEMES_PATH = 'themes'

# Achievement IDs
ACHIEVEMENTS = {
    'first_game': 'First Game',
    'first_128': 'First 128',
    'first_256': 'First 256',
    'first_512': 'First 512',
    'first_1024': 'First 1024',
    'first_2048': 'First 2048',
    'level_5': 'Level 5 Complete',
    'level_10': 'Level 10 Complete',
    'level_15': 'Level 15 Complete',
    'level_20': 'Level 20 Complete',
    'score_1000': 'Score 1000',
    'score_5000': 'Score 5000',
    'score_10000': 'Score 10000',
    'score_50000': 'Score 50000',
    'moves_100': '100 Moves',
    'moves_500': '500 Moves',
    'moves_1000': '1000 Moves',
    'perfect_game': 'Perfect Game',
    'speed_demon': 'Speed Demon',
    'persistent': 'Persistent Player'
}

# Statistics keys
STATISTICS = [
    'games_played',
    'games_won',
    'best_score',
    'total_moves',
    'total_tiles_merged',
    'max_tile_reached',
    'levels_completed',
    'total_time_played',
    'achievements_unlocked',
    'avg_moves_per_game'
]
