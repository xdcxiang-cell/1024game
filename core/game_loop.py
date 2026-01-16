# -*- coding: utf-8 -*-
"""
1024 Game - Main Game Loop
Handles the main game loop with multithreaded rendering and 60FPS control
"""

import pygame
import threading
import queue
import time
import sys

# Ensure core module is in path
sys.path.insert(0, sys.path[0])

# Ensure ui module is in path
sys.path.insert(0, sys.path[0])

# Local imports
from game_logic import Game
from particle_system import ParticleSystem
from audio_system import AudioSystem
from persistence import PersistenceManager, GameProgress


class RenderTask:
    def __init__(self, type, data, priority=0):
        self.type = type
        self.data = data
        self.priority = priority


class RenderThread(threading.Thread):
    """Separate thread for rendering operations"""

    def __init__(self, screen, task_queue, result_queue):
        super().__init__(daemon=True)
        self.screen = screen
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.running = True
        self.particle_system = None
        self.game_screen = None
        self.needs_update = True
        self.lock = threading.Lock()

    def setup(self, particle_system, game_screen):
        """Setup rendering components"""
        self.particle_system = particle_system
        self.game_screen = game_screen

    def run(self):
        """Main rendering loop"""
        while self.running:
            try:
                task = self.task_queue.get(timeout=0.016)  # ~60Hz

                with self.lock:
                    if self.particle_system and self.game_screen:
                        self._process_task(task)

                self.result_queue.put({'type': 'render_complete', 'task': task})

            except queue.Empty:
                continue
            except Exception as e:
                print("Render thread error: %s" % e)

    def _process_task(self, task):
        """Process a rendering task"""
        if task.type == 'render_game':
            game = task.data.get('game')
            settings = task.data.get('settings')
            show_fps = task.data.get('show_fps', False)
            fps = task.data.get('fps', 0)
            state = task.data.get('state', 'playing')

            if game and self.game_screen:
                self.game_screen.render(
                    game, settings, 
                    show_fps=show_fps, fps=fps, state=state
                )

        elif task.type == 'render_menu':
            menu = task.data.get('menu')
            if menu:
                menu.draw(self.screen)

        elif task.type == 'update_particles':
            dt = task.data.get('dt', 0.016)
            if self.particle_system:
                self.particle_system.update(dt)

        elif task.type == 'add_particle_effect':
            effect_type = task.data.get('type')
            x = task.data.get('x', 400)
            y = task.data.get('y', 300)
            value = task.data.get('value', 0)

            if self.particle_system:
                if effect_type == 'merge':
                    self.particle_system.create_merge_effect(x, y, value)
                elif effect_type == 'level_up':
                    self.particle_system.create_level_up_effect(x, y)
                elif effect_type == 'game_over':
                    self.particle_system.create_game_over_effect(x, y)
                elif effect_type == 'score':
                    self.particle_system.create_score_text(x, y, value)

        elif task.type == 'render_particles':
            if self.particle_system:
                self.particle_system.render()

    def stop(self):
        """Stop the rendering thread"""
        self.running = False
        self.join(timeout=1.0)


class GameLoop:
    """Main game loop controller"""

    def __init__(self, width=800, height=600):
        # Import UI components here to avoid circular imports
        from ui.game_screen import GameScreen
        from ui.main_menu import MainMenu

        self.width = width
        self.height = height
        self.screen = None
        self.clock = None

        self.game = None
        self.particle_system = None
        self.audio_system = None
        self.persistence = None
        self.game_screen = None
        self.main_menu = None

        self.render_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.render_thread: Optional[RenderThread] = None

        self.running = False
        self.state = 'menu'  # menu, playing, paused, game_over
        self.target_fps = 60
        self.fps = 0

        self.settings: Dict = {
            'theme': 'default',
            'music_volume': 0.5,
            'sound_volume': 0.7,
            'particle_enabled': True,
            'show_fps': False,
            'enable_3d_sound': True
        }

        self.current_level = 1
        self.achievement_queue: List[str] = []

    def initialize(self):
        """Initialize all game components"""
        pygame.init()
        pygame.display.set_caption("1024 Game")
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.persistence = PersistenceManager()
        self._load_settings()

        self.particle_system = ParticleSystem(self.screen)
        self.audio_system = AudioSystem()
        self.game = Game(level=self.current_level)
        self.game_screen = GameScreen(self.screen, self.settings)
        self.main_menu = MainMenu(self.screen, self._handle_menu_action)

        self.audio_system.set_music_volume(self.settings['music_volume'])
        self.audio_system.set_sound_volume(self.settings['sound_volume'])
        self.audio_system.set_3d_sound_enabled(self.settings['enable_3d_sound'])

        self.render_thread = RenderThread(self.screen, self.render_queue, self.result_queue)
        self.render_thread.setup(self.particle_system, self.game_screen)
        self.render_thread.start()

        self.running = True

    def _load_settings(self):
        """Load saved settings"""
        saved = self.persistence.load_settings()
        if saved:
            self.settings['theme'] = saved.theme
            self.settings['music_volume'] = saved.music_volume
            self.settings['sound_volume'] = saved.sound_volume
            self.settings['particle_enabled'] = saved.particle_enabled
            self.settings['show_fps'] = saved.show_fps
            self.settings['enable_3d_sound'] = saved.enable_3d_sound
            self.target_fps = saved.fps_limit

    def _handle_menu_action(self, action, data=None):
        """Handle menu actions"""
        if action == 'start_game':
            self._start_game()
        elif action == 'select_level':
            if data and 'level' in data:
                self._start_game(level=data['level'])
        elif action == 'show_settings':
            self.main_menu.show_settings(self.settings)
        elif action == 'show_achievements':
            progress = self.persistence.load_progress()
            self.main_menu.show_achievements(progress.achievements if progress else [])
        elif action == 'show_tutorial':
            self.main_menu.show_tutorial()
        elif action == 'update_settings':
            if data:
                self.settings.update(data)
                self._save_settings()
                self.game_screen.update_theme(data.get('theme', self.settings['theme']))
                self.audio_system.set_music_volume(data.get('music_volume', self.settings['music_volume']))
                self.audio_system.set_sound_volume(data.get('sound_volume', self.settings['sound_volume']))
                self.audio_system.set_3d_sound_enabled(data.get('enable_3d_sound', True))
                self.target_fps = data.get('fps_limit', self.target_fps)
        elif action == 'back_to_menu':
            self.state = 'menu'
        elif action == 'quit':
            self.running = False

    def _save_settings(self):
        """Save settings to persistence"""
        if self.persistence:
            # Use dictionary for settings
            settings_data = {
                'theme': self.settings['theme'],
                'music_volume': self.settings['music_volume'],
                'sound_volume': self.settings['sound_volume'],
                'particle_enabled': self.settings['particle_enabled'],
                'fps_limit': self.target_fps,
                'language': 'zh',
                'enable_3d_sound': self.settings['enable_3d_sound'],
                'show_fps': self.settings['show_fps'],
                'tutorial_completed': False
            }
            self.persistence.save_settings(settings_data)

    def _start_game(self, level=1):
        """Start a new game"""
        self.current_level = level
        self.game = Game(level=level)
        self.state = 'playing'
        self.achievement_queue = []

        self.audio_system.play_sound('start')

        # Check achievements
        if self.persistence:
            self.persistence.update_game_stats({'won': False})
            self.persistence.check_achievements({'won': False})

    def _handle_input(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if self.state == 'menu':
                self.main_menu.handle_event(event)

            elif self.state == 'playing':
                if event.type == pygame.KEYDOWN:
                    self._handle_keypress(event.key)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_mouse_click(event.pos)

            elif self.state in ['paused', 'game_over']:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                        if self.state == 'game_over':
                            self.state = 'menu'
                        else:
                            self.state = 'playing'

    def _handle_keypress(self, key):
        """Handle keyboard input"""
        direction = None

        if key == pygame.K_LEFT or key == pygame.K_a:
            direction = 'left'
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            direction = 'right'
        elif key == pygame.K_UP or key == pygame.K_w:
            direction = 'up'
        elif key == pygame.K_DOWN or key == pygame.K_s:
            direction = 'down'
        elif key == pygame.K_ESCAPE:
            self.state = 'paused'
            return
        elif key == pygame.K_r:
            self.game.reset_game(level=self.current_level)
            self.audio_system.play_sound('reset')
            return

        if direction and self.game:
            moved = self.game.move(direction)
            if moved:
                self.audio_system.play_sound('move', x=400, y=300)
                self._add_merge_particles()

                self.game.add_random_tile()

                if self.game.is_level_complete():
                    self._level_complete()

                if self.game.is_game_over():
                    self._game_over()

                self._check_achievements()

    def _handle_mouse_click(self, pos):
        """Handle mouse clicks"""
        pass

    def _add_merge_particles(self):
        """Add merge particle effects"""
        if self.game and self.settings['particle_enabled']:
            for i, row in enumerate(self.game.get_grid()):
                for j, cell in enumerate(row):
                    if cell > 0:
                        if cell in [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]:
                            tile_size = self.game_screen.tile_size
                            x = self.game_screen.grid_x + j * tile_size + tile_size // 2
                            y = self.game_screen.grid_y + i * tile_size + tile_size // 2
                            self.render_queue.put(RenderTask(
                                type='add_particle_effect',
                                data={'type': 'merge', 'x': x, 'y': y, 'value': cell}
                            ))

    def _level_complete(self):
        """Handle level completion"""
        self.state = 'paused'
        self.audio_system.play_sound('level_up')

        if self.settings['particle_enabled']:
            self.render_queue.put(RenderTask(
                type='add_particle_effect',
                data={'type': 'level_up', 'x': 400, 'y': 300}
            ))

        if self.current_level < 20:
            self.current_level += 1

        # Update stats
        if self.persistence:
            stats = self.game.get_stats()
            stats['won'] = True
            self.persistence.update_game_stats(stats)
            unlocked = self.persistence.check_achievements(stats)
            self.achievement_queue.extend(unlocked)

    def _game_over(self):
        """Handle game over"""
        self.state = 'game_over'
        self.audio_system.play_sound('game_over')

        if self.settings['particle_enabled']:
            self.render_queue.put(RenderTask(
                type='add_particle_effect',
                data={'type': 'game_over', 'x': 400, 'y': 300}
            ))

        if self.persistence:
            stats = self.game.get_stats()
            stats['won'] = False
            self.persistence.update_game_stats(stats)

    def _check_achievements(self):
        """Check for new achievements"""
        if self.persistence and self.game:
            stats = self.game.get_stats()
            unlocked = self.persistence.check_achievements(stats)
            for ach_id in unlocked:
                if ach_id not in self.achievement_queue:
                    self.achievement_queue.append(ach_id)
                    self.audio_system.play_sound('achievement')

    def _update(self, dt):
        """Update game state"""
        if self.state == 'playing' and self.game:
            self.game.update_time(dt)

        self.audio_system.update()

        if self.settings['particle_enabled']:
            self.render_queue.put(RenderTask(
                type='update_particles',
                data={'dt': dt}, priority=1
            ))

    def _render(self):
        """Render the game"""
        if self.state == 'menu':
            self.render_queue.put(RenderTask(
                type='render_menu',
                data={'menu': self.main_menu},
                priority=0
            ))
        else:
            self.render_queue.put(RenderTask(
                type='render_game',
                data={
                    'game': self.game,
                    'settings': self.settings,
                    'show_fps': self.settings['show_fps'],
                    'fps': self.fps,
                    'state': self.state
                },
                priority=0
            ))

        # Render particles after game
        if self.settings['particle_enabled']:
            self.render_queue.put(RenderTask(
                type='render_particles',
                data={},
                priority=2
            ))

        pygame.display.flip()

    def run(self):
        """Main game loop"""
        try:
            self.initialize()

            # Pre-fill result queue to prevent blocking
            for _ in range(10):
                self.result_queue.put({'type': 'render_complete'})

            while self.running:
                start_time = time.time()

                self._handle_input()

                if self.running:
                    dt = self.clock.tick(self.target_fps) / 1000.0
                    self.fps = self.clock.get_fps()

                    self._update(dt)
                    self._render()

                    # Clear result queue to prevent overflow
                    while not self.result_queue.empty():
                        try:
                            self.result_queue.get_nowait()
                        except queue.Empty:
                            break

                elapsed = time.time() - start_time
                sleep_time = max(0, 1.0 / self.target_fps - elapsed)
                if sleep_time > 0:
                    time.sleep(sleep_time)

        finally:
            self._cleanup()

    def _cleanup(self):
        """Clean up resources"""
        if self.render_thread:
            self.render_thread.stop()

        pygame.quit()


if __name__ == '__main__':
    game_loop = GameLoop()
    game_loop.run()
