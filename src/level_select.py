import pygame
from typing import List, Optional
from src.ui_components import Button, Label, Panel
from src.level_manager import LevelManager
from src.data_manager import DataManager
from src.config import Config


class LevelSelect:
    def __init__(self, screen_width: int, screen_height: int, font_manager):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_manager = font_manager
        self.level_manager = LevelManager()
        self.data_manager = DataManager()
        self.config = Config()

        self.title_font = font_manager.get_font('title', 48)
        self.button_font = font_manager.get_font('button', 24)

        self.elements = []
        self.level_buttons = []
        self.scroll_offset = 0
        self.max_scroll = 0

        self._create_elements()

        self.on_level_selected = None
        self.on_back = None

    def _create_elements(self):
        colors = self._get_theme_colors()

        self.back_button = Button(
            20, 20, 100, 40,
            "Back", self.button_font,
            colors['button_normal'], colors['button_hover'],
            callback=self._on_back_click
        )

        self.elements = [self.back_button]
        self._create_level_buttons()

    def _get_theme_colors(self):
        theme_name = self.config.get('theme', 'current_theme', default='default')
        theme = self.config.get('theme', 'themes', theme_name, default={})

        return {
            'background': theme.get('background', (187, 173, 160)),
            'button_normal': (143, 122, 102),
            'button_hover': (242, 177, 121),
            'button_disabled': (100, 100, 100),
            'text': theme.get('text', (119, 110, 101))
        }

    def _create_level_buttons(self):
        self.level_buttons = []
        levels = self.level_manager.get_level_progress()

        button_width = 200
        button_height = 60
        button_spacing = 20
        columns = 4
        start_x = (self.screen_width - (columns * (button_width + button_spacing))) // 2 + button_spacing // 2
        start_y = 150

        colors = self._get_theme_colors()

        for i, level_info in enumerate(levels):
            row = i // columns
            col = i % columns

            x = start_x + col * (button_width + button_spacing)
            y = start_y + row * (button_height + button_spacing)

            level = level_info['level']
            unlocked = level_info['unlocked']
            completed = level_info['completed']
            difficulty = level_info['difficulty']

            if unlocked:
                text = f"Level {level}"
                if completed:
                    text += " ✓"
                text += f"\nDiff: {difficulty}"

                button_color = colors['button_normal']
                if completed:
                    button_color = (100, 200, 100)

                button = Button(
                    x, y, button_width, button_height,
                    text, self.button_font,
                    button_color, colors['button_hover'],
                    callback=lambda l=level: self._on_level_click(l)
                )
            else:
                button = Button(
                    x, y, button_width, button_height,
                    f"Level {level}\n🔒", self.button_font,
                    colors['button_disabled'], colors['button_disabled'],
                    enabled=False
                )

            self.level_buttons.append(button)

        total_rows = (len(levels) + columns - 1) // columns
        total_height = total_rows * (button_height + button_spacing)
        self.max_scroll = max(0, total_height - (self.screen_height - 200))

    def _on_level_click(self, level: int):
        if self.on_level_selected:
            self.on_level_selected(level)

    def _on_back_click(self):
        if self.on_back:
            self.on_back()

    def handle_event(self, event):
        if self.back_button.handle_event(event):
            return True

        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset -= event.y * 20
            self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
            self._update_button_positions()
            return True

        for button in self.level_buttons:
            if button.handle_event(event):
                return True

        return False

    def _update_button_positions(self):
        button_height = 60
        button_spacing = 20
        columns = 4
        start_x = (self.screen_width - (columns * (220))) // 2 + 10
        start_y = 150 - self.scroll_offset

        for i, button in enumerate(self.level_buttons):
            row = i // columns
            col = i % columns

            x = start_x + col * 220
            y = start_y + row * (button_height + button_spacing)

            button.rect.x = x
            button.rect.y = y

    def draw(self, surface: pygame.Surface):
        colors = self._get_theme_colors()
        surface.fill(colors['background'])

        title_text = "Select Level"
        title_surface = self.title_font.render(title_text, True, colors['text'])
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 60))
        surface.blit(title_surface, title_rect)

        for element in self.elements:
            element.draw(surface)

        for button in self.level_buttons:
            if 0 <= button.rect.y <= self.screen_height:
                button.draw(surface)

        if self.max_scroll > 0:
            self._draw_scroll_indicator(surface)

    def _draw_scroll_indicator(self, surface: pygame.Surface):
        indicator_height = 100
        indicator_width = 10
        indicator_x = self.screen_width - 30
        indicator_y = (self.screen_height - indicator_height) // 2

        pygame.draw.rect(surface, (100, 100, 100),
                        (indicator_x, indicator_y, indicator_width, indicator_height), border_radius=5)

        scroll_ratio = self.scroll_offset / self.max_scroll
        handle_height = 20
        handle_y = indicator_y + scroll_ratio * (indicator_height - handle_height)

        pygame.draw.rect(surface, (150, 150, 150),
                        (indicator_x, handle_y, indicator_width, handle_height), border_radius=5)

    def refresh(self):
        self._create_level_buttons()
        self._update_button_positions()
