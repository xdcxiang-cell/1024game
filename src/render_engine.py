import pygame
import threading
import queue
import time
from typing import Callable, Optional, List, Tuple
from src.config import Config


class RenderEngine:
    def __init__(self, width: int = 800, height: int = 600, fps: int = 60):
        self.width = width
        self.height = height
        self.fps = fps
        self.running = False
        self.screen = None
        self.clock = None
        self.render_queue = queue.Queue(maxsize=10)
        self.render_thread = None
        self.config = Config()
        self.current_surface = None
        self.frame_count = 0
        self.fps_history = []
        self.target_fps = fps

    def initialize(self):
        pygame.init()
        pygame.display.set_caption("1024 Game - Pygame Edition")

        flags = 0
        if self.config.get('display', 'fullscreen'):
            flags = pygame.FULLSCREEN

        self.screen = pygame.display.set_mode((self.width, self.height), flags)
        self.clock = pygame.time.Clock()
        self.current_surface = pygame.Surface((self.width, self.height))

    def start(self):
        self.running = True
        self.render_thread = threading.Thread(target=self._render_loop, daemon=True)
        self.render_thread.start()

    def stop(self):
        self.running = False
        if self.render_thread:
            self.render_thread.join(timeout=2.0)

    def _render_loop(self):
        while self.running:
            try:
                render_task = self.render_queue.get(timeout=0.016)
                if render_task:
                    self._execute_render(render_task)
                self.render_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Render error: {e}")

    def _execute_render(self, render_task):
        if callable(render_task):
            render_task(self.current_surface)
        elif isinstance(render_task, dict):
            action = render_task.get('action')
            if action == 'blit':
                surface = render_task.get('surface')
                pos = render_task.get('pos', (0, 0))
                if surface:
                    self.current_surface.blit(surface, pos)
            elif action == 'fill':
                color = render_task.get('color', (0, 0, 0))
                self.current_surface.fill(color)
            elif action == 'flip':
                self.screen.blit(self.current_surface, (0, 0))
                pygame.display.flip()
                self.frame_count += 1
                self._update_fps()

    def _update_fps(self):
        current_fps = self.clock.get_fps()
        if current_fps > 0:
            self.fps_history.append(current_fps)
            if len(self.fps_history) > 60:
                self.fps_history.pop(0)

    def get_fps(self) -> float:
        if self.fps_history:
            return sum(self.fps_history) / len(self.fps_history)
        return 0.0

    def submit_render(self, render_task):
        try:
            self.render_queue.put_nowait(render_task)
        except queue.Full:
            pass

    def clear(self, color: Tuple[int, int, int] = (0, 0, 0)):
        self.submit_render({'action': 'fill', 'color': color})

    def blit(self, surface, pos: Tuple[int, int] = (0, 0)):
        self.submit_render({'action': 'blit', 'surface': surface, 'pos': pos})

    def flip(self):
        self.submit_render({'action': 'flip'})

    def render_function(self, func: Callable):
        self.submit_render(func)

    def wait_for_render(self):
        self.render_queue.join()

    def tick(self):
        self.clock.tick(self.target_fps)

    def get_screen(self):
        return self.screen

    def get_surface(self):
        return self.current_surface

    def resize(self, width: int, height: int):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.current_surface = pygame.Surface((self.width, self.height))
