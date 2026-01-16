import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ui_components import Button, Label, Panel, Slider, ProgressBar


class TestButton:
    def test_initialization(self):
        import pygame
        pygame.init()

        font = pygame.font.Font(None, 32)
        button = Button(100, 100, 200, 50, "Test", font, (100, 100, 100), (150, 150, 150))

        assert button.rect.x == 100
        assert button.rect.y == 100
        assert button.rect.width == 200
        assert button.rect.height == 50
        assert button.text == "Test"
        assert button.enabled is True

    def test_hover_state(self):
        import pygame
        pygame.init()

        font = pygame.font.Font(None, 32)
        button = Button(100, 100, 200, 50, "Test", font, (100, 100, 100), (150, 150, 150))

        event = pygame.event.Event(pygame.MOUSEMOTION, {'pos': (200, 125)})
        button.handle_event(event)

        assert button.hovered is True

    def test_click_callback(self):
        import pygame
        pygame.init()

        callback_called = []

        def callback():
            callback_called.append(True)

        font = pygame.font.Font(None, 32)
        button = Button(100, 100, 200, 50, "Test", font, (100, 100, 100), (150, 150, 150), callback=callback)

        button.handle_event(pygame.event.Event(pygame.MOUSEMOTION, {'pos': (200, 125)}))
        button.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (200, 125)}))
        button.handle_event(pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1, 'pos': (200, 125)}))

        assert len(callback_called) == 1

    def test_set_enabled(self):
        import pygame
        pygame.init()

        font = pygame.font.Font(None, 32)
        button = Button(100, 100, 200, 50, "Test", font, (100, 100, 100), (150, 150, 150))

        button.set_enabled(False)

        assert button.enabled is False


class TestLabel:
    def test_initialization(self):
        import pygame
        pygame.init()

        font = pygame.font.Font(None, 32)
        label = Label(100, 100, "Test Label", font)

        assert label.text == "Test Label"
        assert label.visible is True

    def test_set_text(self):
        import pygame
        pygame.init()

        font = pygame.font.Font(None, 32)
        label = Label(100, 100, "Test Label", font)

        label.set_text("New Text")

        assert label.text == "New Text"

    def test_set_visible(self):
        import pygame
        pygame.init()

        font = pygame.font.Font(None, 32)
        label = Label(100, 100, "Test Label", font)

        label.set_visible(False)

        assert label.visible is False


class TestPanel:
    def test_initialization(self):
        panel = Panel(100, 100, 200, 150)

        assert panel.rect.x == 100
        assert panel.rect.y == 100
        assert panel.rect.width == 200
        assert panel.rect.height == 150
        assert panel.visible is True

    def test_custom_colors(self):
        panel = Panel(100, 100, 200, 150, (50, 50, 50), (100, 100, 100), 3)

        assert panel.background_color == (50, 50, 50)
        assert panel.border_color == (100, 100, 100)
        assert panel.border_width == 3

    def test_set_visible(self):
        panel = Panel(100, 100, 200, 150)

        panel.set_visible(False)

        assert panel.visible is False


class TestSlider:
    def test_initialization(self):
        import pygame
        pygame.init()

        font = pygame.font.Font(None, 24)
        slider = Slider(100, 100, 200, 20, 0.0, 1.0, 0.5, font)

        assert slider.rect.x == 100
        assert slider.rect.y == 100
        assert slider.rect.width == 200
        assert slider.rect.height == 20
        assert slider.min_value == 0.0
        assert slider.max_value == 1.0
        assert slider.value == 0.5

    def test_get_value(self):
        import pygame
        pygame.init()

        font = pygame.font.Font(None, 24)
        slider = Slider(100, 100, 200, 20, 0.0, 1.0, 0.5, font)

        value = slider.get_value()

        assert value == 0.5

    def test_set_value(self):
        import pygame
        pygame.init()

        font = pygame.font.Font(None, 24)
        slider = Slider(100, 100, 200, 20, 0.0, 1.0, 0.5, font)

        slider.set_value(0.75)

        assert slider.value == 0.75

    def test_set_value_clamp(self):
        import pygame
        pygame.init()

        font = pygame.font.Font(None, 24)
        slider = Slider(100, 100, 200, 20, 0.0, 1.0, 0.5, font)

        slider.set_value(1.5)

        assert slider.value == 1.0

    def test_dragging(self):
        import pygame
        pygame.init()

        font = pygame.font.Font(None, 24)
        slider = Slider(100, 100, 200, 20, 0.0, 1.0, 0.5, font)

        handle_rect = slider._get_handle_rect()

        slider.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (handle_rect.centerx, handle_rect.centery)}))
        assert slider.dragging is True

        slider.handle_event(pygame.event.Event(pygame.MOUSEMOTION, {'pos': (200, 110)}))
        assert slider.value > 0.5

        slider.handle_event(pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1}))
        assert slider.dragging is False


class TestProgressBar:
    def test_initialization(self):
        bar = ProgressBar(100, 100, 200, 30, 100.0, 50.0)

        assert bar.rect.x == 100
        assert bar.rect.y == 100
        assert bar.rect.width == 200
        assert bar.rect.height == 30
        assert bar.max_value == 100.0
        assert bar.value == 50.0

    def test_set_value(self):
        bar = ProgressBar(100, 100, 200, 30, 100.0, 50.0)

        bar.set_value(75.0)

        assert bar.value == 75.0

    def test_set_value_clamp(self):
        bar = ProgressBar(100, 100, 200, 30, 100.0, 50.0)

        bar.set_value(150.0)

        assert bar.value == 100.0

    def test_set_max_value(self):
        bar = ProgressBar(100, 100, 200, 30, 100.0, 50.0)

        bar.set_max_value(200.0)

        assert bar.max_value == 200.0

    def test_custom_colors(self):
        bar = ProgressBar(100, 100, 200, 30, 100.0, 50.0, (50, 50, 50), (0, 255, 0), (100, 100, 100))

        assert bar.background_color == (50, 50, 50)
        assert bar.fill_color == (0, 255, 0)
        assert bar.border_color == (100, 100, 100)
