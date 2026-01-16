import pygame
from typing import List, Optional
from src.ui_components import Button, Slider, Label, Panel
from src.config import Config
from src.audio_engine import AudioEngine


class Settings:
    def __init__(self, screen_width: int, screen_height: int, font_manager):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_manager = font_manager
        self.config = Config()
        self.audio_engine = AudioEngine()

        self.title_font = font_manager.get_font('title', 48)
        self.button_font = font_manager.get_font('button', 28)
        self.label_font = font_manager.get_font('label', 24)

        self.elements = []
        self.sliders = []
        self.theme_buttons = []

        self._create_elements()

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

        self._create_audio_settings(colors)
        self._create_display_settings(colors)
        self._create_theme_settings(colors)

    def _get_theme_colors(self):
        theme_name = self.config.get('theme', 'current_theme', default='default')
        theme = self.config.get('theme', 'themes', theme_name, default={})

        return {
            'background': theme.get('background', (187, 173, 160)),
            'button_normal': (143, 122, 102),
            'button_hover': (242, 177, 121),
            'text': theme.get('text', (119, 110, 101))
        }

    def _create_audio_settings(self, colors):
        start_y = 120
        slider_width = 300
        slider_height = 20
        slider_spacing = 60

        master_volume = self.config.get('audio', 'volume', default=0.7)
        sfx_volume = self.config.get('audio', 'sfx_volume', default=0.8)

        self.master_volume_slider = Slider(
            200, start_y, slider_width, slider_height,
            0.0, 1.0, master_volume, self.label_font
        )

        self.sfx_volume_slider = Slider(
            200, start_y + slider_spacing, slider_width, slider_height,
            0.0, 1.0, sfx_volume, self.label_font
        )

        self.sliders = [self.master_volume_slider, self.sfx_volume_slider]

        self.audio_enabled_button = Button(
            550, start_y, 120, 40,
            "On" if self.config.get('audio', 'enabled', default=True) else "Off",
            self.button_font,
            colors['button_normal'], colors['button_hover'],
            callback=self._toggle_audio
        )

        self.elements.append(self.audio_enabled_button)

    def _create_display_settings(self, colors):
        start_y = 300
        slider_width = 300
        slider_height = 20

        self.fps_slider = Slider(
            200, start_y, slider_width, slider_height,
            30, 120, self.config.get('display', 'fps', default=60), self.label_font
        )

        self.sliders.append(self.fps_slider)

        self.fullscreen_button = Button(
            550, start_y, 120, 40,
            "On" if self.config.get('display', 'fullscreen', default=False) else "Off",
            self.button_font,
            colors['button_normal'], colors['button_hover'],
            callback=self._toggle_fullscreen
        )

        self.elements.append(self.fullscreen_button)

    def _create_theme_settings(self, colors):
        start_y = 400
        themes = self.config.get('theme', 'themes', default={})
        current_theme = self.config.get('theme', 'current_theme', default='default')

        x = 200
        for theme_name in themes.keys():
            theme_button = Button(
                x, start_y, 100, 40,
                theme_name.capitalize(), self.button_font,
                colors['button_normal'], colors['button_hover'],
                callback=lambda t=theme_name: self._set_theme(t)
            )

            if theme_name == current_theme:
                theme_button.normal_color = (100, 200, 100)

            self.theme_buttons.append(theme_button)
            x += 120

        self.elements.extend(self.theme_buttons)

    def _on_back_click(self):
        self._save_settings()
        if self.on_back:
            self.on_back()

    def _toggle_audio(self):
        current = self.config.get('audio', 'enabled', default=True)
        self.config.set('audio', 'enabled', value=not current)
        self.audio_engine.set_enabled(not current)
        self.audio_engine.play_ui('click')
        self._create_elements()

    def _toggle_fullscreen(self):
        current = self.config.get('display', 'fullscreen', default=False)
        self.config.set('display', 'fullscreen', value=not current)
        self._create_elements()

    def _set_theme(self, theme_name: str):
        self.config.set('theme', 'current_theme', value=theme_name)
        self._create_elements()

    def _save_settings(self):
        self.config.set('audio', 'volume', value=self.master_volume_slider.get_value())
        self.config.set('audio', 'sfx_volume', value=self.sfx_volume_slider.get_value())
        self.config.set('display', 'fps', value=int(self.fps_slider.get_value()))

        self.audio_engine.set_master_volume(self.master_volume_slider.get_value())
        self.audio_engine.set_sfx_volume(self.sfx_volume_slider.get_value())

        self.config.save()

    def handle_event(self, event):
        for element in self.elements:
            if element.handle_event(event):
                return True

        for slider in self.sliders:
            if slider.handle_event(event):
                return True

        return False

    def draw(self, surface: pygame.Surface):
        colors = self._get_theme_colors()
        surface.fill(colors['background'])

        title_text = "Settings"
        title_surface = self.title_font.render(title_text, True, colors['text'])
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 60))
        surface.blit(title_surface, title_rect)

        for element in self.elements:
            element.draw(surface)

        for slider in self.sliders:
            slider.draw(surface)

        self._draw_labels(surface)

    def _draw_labels(self, surface: pygame.Surface):
        colors = self._get_theme_colors()

        labels = [
            ("Audio", 100),
            ("Master Volume", 150),
            ("SFX Volume", 210),
            ("Display", 280),
            ("FPS", 330),
            ("Fullscreen", 330),
            ("Theme", 380)
        ]

        for text, y in labels:
            label_surface = self.label_font.render(text, True, colors['text'])
            surface.blit(label_surface, (50, y))
