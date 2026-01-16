import pygame
from typing import Tuple, Optional, Callable
from src.config import Config


class Button:
    def __init__(self, x: int, y: int, width: int, height: int,
                 text: str, font: pygame.font.Font,
                 normal_color: Tuple[int, int, int],
                 hover_color: Tuple[int, int, int],
                 text_color: Tuple[int, int, int] = (255, 255, 255),
                 callback: Optional[Callable] = None,
                 enabled: bool = True):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.callback = callback
        self.hovered = False
        self.clicked = False
        self.enabled = enabled

    def handle_event(self, event) -> bool:
        if not self.enabled:
            return False

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.hovered:
                self.clicked = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.clicked and self.hovered:
                if self.callback:
                    self.callback()
                self.clicked = False
                return True
            self.clicked = False

        return False

    def draw(self, surface: pygame.Surface):
        if not self.enabled:
            color = tuple(c // 2 for c in self.normal_color)
        else:
            color = self.hover_color if self.hovered else self.normal_color

        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=8)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def set_enabled(self, enabled: bool):
        self.enabled = enabled

    def set_callback(self, callback: Callable):
        self.callback = callback


class UIElement:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True

    def handle_event(self, event) -> bool:
        return False

    def draw(self, surface: pygame.Surface):
        pass

    def set_visible(self, visible: bool):
        self.visible = visible


class Panel(UIElement):
    def __init__(self, x: int, y: int, width: int, height: int,
                 background_color: Tuple[int, int, int] = (50, 50, 50),
                 border_color: Tuple[int, int, int] = (100, 100, 100),
                 border_width: int = 2):
        super().__init__(x, y, width, height)
        self.background_color = background_color
        self.border_color = border_color
        self.border_width = border_width

    def draw(self, surface: pygame.Surface):
        if not self.visible:
            return

        pygame.draw.rect(surface, self.background_color, self.rect, border_radius=10)
        if self.border_width > 0:
            pygame.draw.rect(surface, self.border_color, self.rect,
                           self.border_width, border_radius=10)


class Label(UIElement):
    def __init__(self, x: int, y: int, text: str, font: pygame.font.Font,
                 text_color: Tuple[int, int, int] = (255, 255, 255)):
        super().__init__(x, y, 0, 0)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.update_rect()

    def update_rect(self):
        text_surface = self.font.render(self.text, True, self.text_color)
        self.rect = text_surface.get_rect(topleft=(self.rect.x, self.rect.y))

    def set_text(self, text: str):
        self.text = text
        self.update_rect()

    def draw(self, surface: pygame.Surface):
        if not self.visible:
            return

        text_surface = self.font.render(self.text, True, self.text_color)
        surface.blit(text_surface, self.rect.topleft)


class Slider(UIElement):
    def __init__(self, x: int, y: int, width: int, height: int,
                 min_value: float, max_value: float, initial_value: float,
                 font: pygame.font.Font):
        super().__init__(x, y, width, height)
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.font = font
        self.dragging = False
        self.handle_width = 20

    def handle_event(self, event) -> bool:
        if not self.visible:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                handle_rect = self._get_handle_rect()
                if handle_rect.collidepoint(event.pos):
                    self.dragging = True
                elif self.rect.collidepoint(event.pos):
                    self._update_value_from_pos(event.pos[0])
                    self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self._update_value_from_pos(event.pos[0])
                return True

        return False

    def _get_handle_rect(self) -> pygame.Rect:
        ratio = (self.value - self.min_value) / (self.max_value - self.min_value)
        handle_x = self.rect.x + ratio * (self.rect.width - self.handle_width)
        return pygame.Rect(handle_x, self.rect.y, self.handle_width, self.rect.height)

    def _update_value_from_pos(self, x: int):
        relative_x = x - self.rect.x
        ratio = max(0, min(1, relative_x / (self.rect.width - self.handle_width)))
        self.value = self.min_value + ratio * (self.max_value - self.min_value)

    def get_value(self) -> float:
        return self.value

    def set_value(self, value: float):
        self.value = max(self.min_value, min(self.max_value, value))

    def draw(self, surface: pygame.Surface):
        if not self.visible:
            return

        pygame.draw.rect(surface, (100, 100, 100), self.rect, border_radius=5)

        handle_rect = self._get_handle_rect()
        pygame.draw.rect(surface, (150, 150, 150), handle_rect, border_radius=5)

        value_text = f"{self.value:.2f}"
        text_surface = self.font.render(value_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(midleft=(self.rect.right + 10, self.rect.centery))
        surface.blit(text_surface, text_rect)


class ProgressBar(UIElement):
    def __init__(self, x: int, y: int, width: int, height: int,
                 max_value: float, initial_value: float = 0.0,
                 background_color: Tuple[int, int, int] = (50, 50, 50),
                 fill_color: Tuple[int, int, int] = (0, 200, 0),
                 border_color: Tuple[int, int, int] = (100, 100, 100)):
        super().__init__(x, y, width, height)
        self.max_value = max_value
        self.value = initial_value
        self.background_color = background_color
        self.fill_color = fill_color
        self.border_color = border_color

    def set_value(self, value: float):
        self.value = max(0, min(self.max_value, value))

    def set_max_value(self, max_value: float):
        self.max_value = max_value

    def get_value(self) -> float:
        return self.value

    def draw(self, surface: pygame.Surface):
        if not self.visible:
            return

        pygame.draw.rect(surface, self.background_color, self.rect, border_radius=5)
        pygame.draw.rect(surface, self.border_color, self.rect, 2, border_radius=5)

        if self.max_value > 0:
            fill_width = int((self.value / self.max_value) * self.rect.width)
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
            pygame.draw.rect(surface, self.fill_color, fill_rect, border_radius=5)
