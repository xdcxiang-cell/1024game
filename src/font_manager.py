import pygame
from typing import Dict, Optional


class FontManager:
    def __init__(self):
        self.fonts: Dict[str, pygame.font.Font] = {}
        self.font_sizes = {
            'title': 60,
            'subtitle': 48,
            'button': 32,
            'label': 24,
            'small': 18
        }

    def get_font(self, name: str, size: Optional[int] = None) -> pygame.font.Font:
        if size is None:
            size = self.font_sizes.get(name, 24)

        key = f"{name}_{size}"

        if key not in self.fonts:
            try:
                self.fonts[key] = pygame.font.Font(None, size)
            except pygame.error:
                self.fonts[key] = pygame.font.SysFont('Arial', size)

        return self.fonts[key]

    def set_font_size(self, name: str, size: int):
        self.font_sizes[name] = size

    def clear_cache(self):
        self.fonts.clear()

    def preload_fonts(self, sizes: Dict[str, int]):
        for name, size in sizes.items():
            self.get_font(name, size)
