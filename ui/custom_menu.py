# -*- coding: utf-8 -*-
"""Custom Menu System - Pure Pygame implementation without pygame_menu"""

import pygame


class Button:
    """Custom button widget"""
    
    def __init__(self, text, x, y, width, height, 
                 bg_color=(205, 193, 180), hover_color=(242, 177, 121),
                 text_color=(119, 110, 101), hover_text_color=(255, 255, 255),
                 font_size=30, callback=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hover_text_color = hover_text_color
        self.font_size = font_size
        self.callback = callback
        
        self.rect = pygame.Rect(x, y, width, height)
        self.hovered = False
        self.font = pygame.font.Font(None, font_size)
    
    def handle_event(self, event):
        """Handle mouse events"""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.hovered:
                if self.callback:
                    self.callback()
                return True
        return False
    
    def draw(self, screen):
        """Draw button on screen"""
        color = self.hover_color if self.hovered else self.bg_color
        text_color = self.hover_text_color if self.hovered else self.text_color
        
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, (119, 110, 101), self.rect, 2, border_radius=5)
        
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def set_text(self, text):
        """Update button text"""
        self.text = text


class Label:
    """Custom label widget"""
    
    def __init__(self, text, x, y, font_size=24, color=(119, 110, 101),
                 font=None, bold=False):
        self.text = text
        self.x = x
        self.y = y
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.Font(font, font_size)
        if bold:
            self.font.set_bold(True)
        
        self.surface = self.font.render(text, True, color)
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw(self, screen):
        """Draw label on screen"""
        screen.blit(self.surface, self.rect)
    
    def set_text(self, text):
        """Update label text"""
        self.text = text
        self.surface = self.font.render(text, True, self.color)
        self.rect = self.surface.get_rect()
        self.rect.x = self.x
        self.rect.y = y


class Slider:
    """Custom slider widget for value selection"""
    
    def __init__(self, text, x, y, width, min_val, max_val, default_val,
                 steps=None, callback=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.min_val = min_val
        self.max_val = max_val
        self.value = default_val
        self.steps = steps
        self.callback = callback
        
        self.knob_radius = 12
        self.knob_x = x + int((default_val - min_val) / (max_val - min_val) * width)
        self.dragging = False
        
        self.font = pygame.font.Font(None, 24)
        self.label = Label(text, x, y - 30, font_size=24)
    
    def handle_event(self, event):
        """Handle mouse events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                knob_rect = pygame.Rect(
                    self.knob_x - self.knob_radius,
                    self.y - self.knob_radius,
                    self.knob_radius * 2,
                    self.knob_radius * 2
                )
                if knob_rect.collidepoint(event.pos):
                    self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.knob_x = max(self.x, min(self.x + self.width, event.pos[0]))
                self._update_value()
    
    def _update_value(self):
        """Update value based on knob position"""
        ratio = (self.knob_x - self.x) / self.width
        self.value = self.min_val + ratio * (self.max_val - self.min_val)
        
        if self.steps:
            self.value = min(self.steps, key=lambda x: abs(x - self.value))
            self.knob_x = self.x + int((self.value - self.min_val) / (self.max_val - self.min_val) * self.width)
        
        if self.callback:
            self.callback(self.value)
    
    def draw(self, screen):
        """Draw slider on screen"""
        self.label.draw(screen)
        
        pygame.draw.rect(screen, (187, 173, 160), (self.x, self.y, self.width, 8))
        pygame.draw.rect(screen, (242, 177, 121), (self.x, self.y, self.knob_x - self.x, 8))
        
        pygame.draw.circle(screen, (246, 94, 59), (self.knob_x, self.y), self.knob_radius)
        pygame.draw.circle(screen, (255, 255, 255), (self.knob_x, self.y), self.knob_radius - 2)
        
        value_text = self.font.render(f"{int(self.value * 100)}%" if self.value <= 1 else str(self.value), True, (119, 110, 101))
        screen.blit(value_text, (self.x + self.width + 10, self.y - 10))
    
    def get_value(self):
        """Get current slider value"""
        return self.value


class ToggleSwitch:
    """Custom toggle switch widget"""
    
    def __init__(self, text, x, y, default=False, callback=None):
        self.text = text
        self.x = x
        self.y = y
        self.value = default
        self.callback = callback
        
        self.switch_rect = pygame.Rect(x + 200, y, 60, 30)
        self.knob_rect = pygame.Rect(x + 200 + (30 if default else 0), y + 3, 24, 24)
        
        self.font = pygame.font.Font(None, 24)
    
    def handle_event(self, event):
        """Handle mouse events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.switch_rect.collidepoint(event.pos):
                    self.value = not self.value
                    self.knob_rect.x = self.x + 200 + (30 if self.value else 0)
                    if self.callback:
                        self.callback(self.value)
                    return True
        return False
    
    def draw(self, screen):
        """Draw toggle switch on screen"""
        text_surf = self.font.render(self.text, True, (119, 110, 101))
        screen.blit(text_surf, (self.x, self.y))
        
        bg_color = (143, 240, 164) if self.value else (187, 173, 160)
        pygame.draw.rect(screen, bg_color, self.switch_rect, border_radius=15)
        pygame.draw.circle(screen, (255, 255, 255), self.knob_rect.center, 12)
    
    def get_value(self):
        """Get current toggle value"""
        return self.value


class Selector:
    """Custom selector widget for option selection"""
    
    def __init__(self, text, x, y, options, default_index=0, callback=None):
        self.text = text
        self.x = x
        self.y = y
        self.options = options
        self.current_index = default_index
        self.callback = callback
        
        self.font = pygame.font.Font(None, 24)
        self.dropdown_open = False
    
    def handle_event(self, event):
        """Handle mouse events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                label_rect = pygame.Rect(self.x, self.y - 30, 200, 30)
                if label_rect.collidepoint(event.pos):
                    self.dropdown_open = not self.dropdown_open
                elif self.dropdown_open:
                    for i, opt in enumerate(self.options):
                        option_rect = pygame.Rect(self.x, self.y + i * 30, 200, 30)
                        if option_rect.collidepoint(event.pos):
                            self.current_index = i
                            self.dropdown_open = False
                            if self.callback:
                                self.callback(self.get_value())
                            return True
    
    def draw(self, screen):
        """Draw selector on screen"""
        text_surf = self.font.render(self.text, True, (119, 110, 101))
        screen.blit(text_surf, (self.x, self.y - 30))
        
        current_text = self.options[self.current_index][0]
        current_surf = self.font.render(current_text, True, (255, 255, 255))
        pygame.draw.rect(screen, (205, 193, 180), (self.x, self.y, 200, 30))
        pygame.draw.rect(screen, (119, 110, 101), (self.x, self.y, 200, 30), 2)
        screen.blit(current_surf, (self.x + 5, self.y + 3))
        
        if self.dropdown_open:
            for i, opt in enumerate(self.options):
                option_rect = pygame.Rect(self.x, self.y + (i + 1) * 30, 200, 30)
                if i == self.current_index:
                    pygame.draw.rect(screen, (242, 177, 121), option_rect)
                else:
                    pygame.draw.rect(screen, (220, 210, 200), option_rect)
                
                opt_surf = self.font.render(opt[0], True, (119, 110, 101))
                screen.blit(opt_surf, (self.x + 5, self.y + (i + 1) * 30 + 3))
    
    def get_value(self):
        """Get current selected value"""
        return self.options[self.current_index][1]
    
    def set_value(self, value):
        """Set selector value"""
        for i, opt in enumerate(self.options):
            if opt[1] == value:
                self.current_index = i
                break


class Menu:
    """Base menu class"""
    
    def __init__(self, screen, title):
        self.screen = screen
        self.title = title
        self.widgets = []
        self.running = True
        
        self.font = pygame.font.Font(None, 48)
        self.title_font = pygame.font.Font(None, 64)
    
    def add_button(self, text, x, y, width, height, callback=None, **kwargs):
        """Add a button to the menu"""
        btn = Button(text, x, y, width, height, callback=callback, **kwargs)
        self.widgets.append(btn)
        return btn
    
    def add_label(self, text, x, y, **kwargs):
        """Add a label to the menu"""
        label = Label(text, x, y, **kwargs)
        self.widgets.append(label)
        return label
    
    def add_slider(self, text, x, y, width, min_val, max_val, default_val, **kwargs):
        """Add a slider to the menu"""
        slider = Slider(text, x, y, width, min_val, max_val, default_val, **kwargs)
        self.widgets.append(slider)
        return slider
    
    def add_toggle(self, text, x, y, default=False, **kwargs):
        """Add a toggle switch to the menu"""
        toggle = ToggleSwitch(text, x, y, default=default, **kwargs)
        self.widgets.append(toggle)
        return toggle
    
    def add_selector(self, text, x, y, options, **kwargs):
        """Add a selector to the menu"""
        selector = Selector(text, x, y, options, **kwargs)
        self.widgets.append(selector)
        return selector
    
    def handle_event(self, event):
        """Handle events for all widgets"""
        for widget in self.widgets:
            if hasattr(widget, 'handle_event'):
                if widget.handle_event(event):
                    return True
        return False
    
    def draw(self):
        """Draw menu and all widgets"""
        self.screen.fill((187, 173, 160))
        
        title_surf = self.title_font.render(self.title, True, (255, 255, 255))
        title_rect = title_surf.get_rect(centerx=self.screen.get_width() // 2, y=40)
        pygame.draw.rect(self.screen, (242, 177, 121), title_rect.inflate(40, 20))
        self.screen.blit(title_surf, title_rect)
        
        for widget in self.widgets:
            widget.draw(self.screen)
    
    def is_running(self):
        """Check if menu is running"""
        return self.running
    
    def stop(self):
        """Stop the menu"""
        self.running = False


class MainMenuScreen:
    """Main menu screen"""
    
    def __init__(self, screen, on_start, on_level_select, on_settings, on_achievements, on_tutorial, on_quit):
        self.screen = screen
        self.on_start = on_start
        self.on_level_select = on_level_select
        self.on_settings = on_settings
        self.on_achievements = on_achievements
        self.on_tutorial = on_tutorial
        self.on_quit = on_quit
        
        self.running = True
        self.widgets = []
        self._create_widgets()
    
    def _create_widgets(self):
        """Create main menu widgets"""
        width = self.screen.get_width()
        height = self.screen.get_height()
        
        btn_width = 250
        btn_height = 50
        btn_y = 200
        btn_spacing = 70
        
        self.widgets.append(Button(
            "Start Game",
            (width - btn_width) // 2, btn_y,
            btn_width, btn_height,
            callback=lambda: self._handle_action('start')
        ))
        
        self.widgets.append(Button(
            "Level Select",
            (width - btn_width) // 2, btn_y + btn_spacing,
            btn_width, btn_height,
            callback=lambda: self._handle_action('level_select')
        ))
        
        self.widgets.append(Button(
            "Settings",
            (width - btn_width) // 2, btn_y + btn_spacing * 2,
            btn_width, btn_height,
            callback=lambda: self._handle_action('settings')
        ))
        
        self.widgets.append(Button(
            "Achievements",
            (width - btn_width) // 2, btn_y + btn_spacing * 3,
            btn_width, btn_height,
            callback=lambda: self._handle_action('achievements')
        ))
        
        self.widgets.append(Button(
            "Tutorial",
            (width - btn_width) // 2, btn_y + btn_spacing * 4,
            btn_width, btn_height,
            callback=lambda: self._handle_action('tutorial')
        ))
        
        self.widgets.append(Button(
            "Quit",
            (width - btn_width) // 2, btn_y + btn_spacing * 5,
            btn_width, btn_height,
            bg_color=(246, 124, 95),
            hover_color=(246, 94, 59),
            callback=lambda: self._handle_action('quit')
        ))
        
        self.widgets.append(Label(
            "Version 2.0 - Pygame Edition",
            (width - 200) // 2,
            height - 50,
            font_size=20,
            color=(150, 150, 150)
        ))
    
    def _handle_action(self, action):
        """Handle menu actions"""
        self.running = False
        if action == 'start':
            self.on_start()
        elif action == 'level_select':
            self.on_level_select()
        elif action == 'settings':
            self.on_settings()
        elif action == 'achievements':
            self.on_achievements()
        elif action == 'tutorial':
            self.on_tutorial()
        elif action == 'quit':
            self.on_quit()
    
    def handle_event(self, event):
        """Handle mouse events"""
        for widget in self.widgets:
            if hasattr(widget, 'handle_event'):
                widget.handle_event(event)
    
    def draw(self, screen):
        """Draw main menu"""
        screen.fill((187, 173, 160))
        
        title_font = pygame.font.Font(None, 72)
        title_surf = title_font.render("1024 Game", True, (255, 255, 255))
        title_rect = title_surf.get_rect(centerx=screen.get_width() // 2, y=60)
        pygame.draw.rect(screen, (242, 177, 121), title_rect.inflate(60, 30))
        screen.blit(title_surf, title_rect)
        
        for widget in self.widgets:
            widget.draw(screen)
    
    def is_running(self):
        """Check if menu is running"""
        return self.running
    
    def reset(self):
        """Reset menu state"""
        self.running = True


class LevelSelectScreen:
    """Level selection screen"""
    
    def __init__(self, screen, on_select, on_back, unlocked_levels=1):
        self.screen = screen
        self.on_select = on_select
        self.on_back = on_back
        self.unlocked_levels = unlocked_levels
        self.total_levels = 20
        
        self.running = True
        self.widgets = []
        self._create_widgets()
    
    def _create_widgets(self):
        """Create level select widgets"""
        width = self.screen.get_width()
        height = self.screen.get_height()
        
        levels_per_row = 5
        btn_size = 60
        spacing = 20
        start_x = (width - (levels_per_row * (btn_size + spacing) - spacing)) // 2
        start_y = 120
        
        for level in range(1, self.total_levels + 1):
            row = (level - 1) // levels_per_row
            col = (level - 1) % levels_per_row
            x = start_x + col * (btn_size + spacing)
            y = start_y + row * (btn_size + spacing)
            
            is_unlocked = level <= self.unlocked_levels
            
            if is_unlocked:
                tier = (level - 1) // 5
                colors = [
                    (143, 240, 164),   # Easy (green)
                    (242, 177, 121),   # Medium (orange)
                    (246, 124, 95),    # Hard (red)
                    (246, 94, 59)      # Expert (dark red)
                ]
                
                self.widgets.append(Button(
                    str(level),
                    x, y, btn_size, btn_size,
                    bg_color=colors[tier],
                    hover_color=(255, 255, 255),
                    text_color=(255, 255, 255),
                    hover_text_color=colors[tier],
                    font_size=28,
                    callback=lambda l=level: self._select_level(l)
                ))
            else:
                self.widgets.append(Button(
                    "?",
                    x, y, btn_size, btn_size,
                    bg_color=(120, 120, 120),
                    text_color=(80, 80, 80),
                    font_size=28,
                    callback=None
                ))
        
        self.widgets.append(Button(
            "Back",
            (width - 150) // 2,
            height - 80,
            150, 45,
            callback=self._go_back
        ))
        
        self.widgets.append(Label(
            "Easy", 100, height - 140, font_size=18, color=(143, 240, 164)
        ))
        self.widgets.append(Label(
            "Medium", 180, height - 140, font_size=18, color=(242, 177, 121)
        ))
        self.widgets.append(Label(
            "Hard", 300, height - 140, font_size=18, color=(246, 124, 95)
        ))
        self.widgets.append(Label(
            "Expert", 400, height - 140, font_size=18, color=(246, 94, 59)
        ))
    
    def _select_level(self, level):
        """Handle level selection"""
        self.running = False
        self.on_select(level)
    
    def _go_back(self):
        """Go back to main menu"""
        self.running = False
        self.on_back()
    
    def handle_event(self, event):
        """Handle mouse events"""
        for widget in self.widgets:
            if hasattr(widget, 'handle_event'):
                widget.handle_event(event)
    
    def draw(self, screen):
        """Draw level select screen"""
        screen.fill((187, 173, 160))
        
        title_font = pygame.font.Font(None, 56)
        title_surf = title_font.render("Select Level", True, (255, 255, 255))
        title_rect = title_surf.get_rect(centerx=screen.get_width() // 2, y=40)
        pygame.draw.rect(screen, (242, 177, 121), title_rect.inflate(40, 20))
        screen.blit(title_surf, title_rect)
        
        for widget in self.widgets:
            widget.draw(screen)
    
    def is_running(self):
        """Check if menu is running"""
        return self.running
    
    def reset(self):
        """Reset menu state"""
        self.running = True


class SettingsScreen:
    """Settings screen"""
    
    def __init__(self, screen, on_save, on_back, initial_settings):
        self.screen = screen
        self.on_save = on_save
        self.on_back = on_back
        self.settings = initial_settings
        
        self.running = True
        self.widgets = []
        self._create_widgets()
    
    def _create_widgets(self):
        """Create settings widgets"""
        width = self.screen.get_width()
        
        y = 120
        spacing = 60
        
        self.widgets.append(Label(
            "Audio Settings", 200, y - 40, font_size=32, color=(255, 255, 255)
        ))
        
        self.music_slider = Slider(
            "Music Volume:", 150, y, 300, 0, 1, self.settings.get('music_volume', 0.5)
        )
        self.widgets.append(self.music_slider)
        
        y += spacing
        self.sound_slider = Slider(
            "Sound Volume:", 150, y, 300, 0, 1, self.settings.get('sound_volume', 0.7)
        )
        self.widgets.append(self.sound_slider)
        
        y += spacing + 20
        self.widgets.append(Label(
            "Graphics Settings", 200, y - 40, font_size=32, color=(255, 255, 255)
        ))
        
        y += spacing
        self.fps_selector = Selector(
            "FPS Limit:", 150, y,
            [("30", 30), ("60", 60), ("120", 120)],
            default_index=1 if self.settings.get('fps_limit', 60) == 60 else 0
        )
        self.widgets.append(self.fps_selector)
        
        y += spacing
        self.particle_toggle = ToggleSwitch(
            "Particle Effects:", 150, y,
            default=self.settings.get('particle_enabled', True)
        )
        self.widgets.append(self.particle_toggle)
        
        y += spacing
        self.sound_3d_toggle = ToggleSwitch(
            "3D Sound:", 150, y,
            default=self.settings.get('enable_3d_sound', True)
        )
        self.widgets.append(self.sound_3d_toggle)
        
        y += spacing
        self.fps_show_toggle = ToggleSwitch(
            "Show FPS:", 150, y,
            default=self.settings.get('show_fps', False)
        )
        self.widgets.append(self.fps_show_toggle)
        
        y += spacing + 20
        self.widgets.append(Label(
            "Theme Settings", 200, y - 40, font_size=32, color=(255, 255, 255)
        ))
        
        y += spacing
        self.theme_selector = Selector(
            "Theme:", 150, y,
            [("Default", "default"), ("Dark", "dark"), ("Ocean", "ocean"), ("Sunset", "sunset")],
            default_index=0
        )
        self.widgets.append(self.theme_selector)
        
        y += spacing + 40
        self.widgets.append(Button(
            "Save",
            (width - 320) // 2, y,
            150, 45,
            bg_color=(143, 240, 164),
            callback=self._save_settings
        ))
        
        self.widgets.append(Button(
            "Back",
            (width + 20) // 2, y,
            150, 45,
            callback=self._go_back
        ))
    
    def _save_settings(self):
        """Save settings"""
        self.settings['music_volume'] = self.music_slider.get_value()
        self.settings['sound_volume'] = self.sound_slider.get_value()
        self.settings['fps_limit'] = self.fps_selector.get_value()
        self.settings['particle_enabled'] = self.particle_toggle.get_value()
        self.settings['enable_3d_sound'] = self.sound_3d_toggle.get_value()
        self.settings['show_fps'] = self.fps_show_toggle.get_value()
        self.settings['theme'] = self.theme_selector.get_value()
        
        self.running = False
        self.on_save(self.settings)
    
    def _go_back(self):
        """Go back to main menu"""
        self.running = False
        self.on_back()
    
    def handle_event(self, event):
        """Handle mouse events"""
        for widget in self.widgets:
            if hasattr(widget, 'handle_event'):
                widget.handle_event(event)
    
    def draw(self, screen):
        """Draw settings screen"""
        screen.fill((187, 173, 160))
        
        title_font = pygame.font.Font(None, 56)
        title_surf = title_font.render("Settings", True, (255, 255, 255))
        title_rect = title_surf.get_rect(centerx=screen.get_width() // 2, y=40)
        pygame.draw.rect(screen, (242, 177, 121), title_rect.inflate(40, 20))
        screen.blit(title_surf, title_rect)
        
        for widget in self.widgets:
            widget.draw(screen)
    
    def is_running(self):
        """Check if menu is running"""
        return self.running
    
    def reset(self):
        """Reset menu state"""
        self.running = True


class AchievementScreen:
    """Achievements screen"""
    
    def __init__(self, screen, on_back, achievements):
        self.screen = screen
        self.on_back = on_back
        self.achievements = achievements
        
        self.running = True
        self.widgets = []
        self._create_widgets()
    
    def _create_widgets(self):
        """Create achievements widgets"""
        width = self.screen.get_width()
        height = self.screen.get_height()
        
        y = 120
        spacing = 50
        
        total = len(self.achievements)
        unlocked = sum(1 for a in self.achievements.values() if a.get('unlocked', False))
        
        self.widgets.append(Label(
            f"Progress: {unlocked}/{total}",
            (width - 200) // 2, y - 60,
            font_size=28, color=(255, 255, 255)
        ))
        
        for ach_id, data in self.achievements.items():
            name = data.get('name', 'Unknown')
            desc = data.get('description', '')
            unlocked = data.get('unlocked', False)
            
            color = (143, 240, 164) if unlocked else (150, 150, 150)
            check = "✓" if unlocked else "  "
            
            self.widgets.append(Label(
                f"{check} {name}",
                100, y,
                font_size=24, color=color
            ))
            
            self.widgets.append(Label(
                f"  {desc}",
                100, y + 30,
                font_size=18, color=(120, 120, 120) if unlocked else (100, 100, 100)
            ))
            
            y += spacing
        
        self.widgets.append(Button(
            "Back",
            (width - 150) // 2,
            height - 80,
            150, 45,
            callback=self._go_back
        ))
    
    def _go_back(self):
        """Go back to main menu"""
        self.running = False
        self.on_back()
    
    def handle_event(self, event):
        """Handle mouse events"""
        for widget in self.widgets:
            if hasattr(widget, 'handle_event'):
                widget.handle_event(event)
    
    def draw(self, screen):
        """Draw achievements screen"""
        screen.fill((187, 173, 160))
        
        title_font = pygame.font.Font(None, 56)
        title_surf = title_font.render("Achievements", True, (255, 255, 255))
        title_rect = title_surf.get_rect(centerx=screen.get_width() // 2, y=40)
        pygame.draw.rect(screen, (242, 177, 121), title_rect.inflate(40, 20))
        screen.blit(title_surf, title_rect)
        
        for widget in self.widgets:
            widget.draw(screen)
    
    def is_running(self):
        """Check if menu is running"""
        return self.running
    
    def reset(self):
        """Reset menu state"""
        self.running = True


class TutorialScreen:
    """Tutorial screen"""
    
    def __init__(self, screen, on_back):
        self.screen = screen
        self.on_back = on_back
        
        self.running = True
        self.widgets = []
        self._create_widgets()
    
    def _create_widgets(self):
        """Create tutorial widgets"""
        width = self.screen.get_width()
        height = self.screen.get_height()
        
        y = 100
        
        self.widgets.append(Label(
            "How to Play",
            (width - 200) // 2, y - 40,
            font_size=32, color=(255, 255, 255)
        ))
        
        y += 60
        self.widgets.append(Label(
            "1. Use Arrow Keys or WASD to move tiles",
            80, y,
            font_size=24, color=(255, 255, 255)
        ))
        
        y += 40
        self.widgets.append(Label(
            "2. When two tiles with the same number touch, they merge",
            80, y,
            font_size=24, color=(255, 255, 255)
        ))
        
        y += 40
        self.widgets.append(Label(
            "3. Each level has a target value - reach it to advance",
            80, y,
            font_size=24, color=(255, 255, 255)
        ))
        
        y += 40
        self.widgets.append(Label(
            "4. Press R to restart, ESC to pause",
            80, y,
            font_size=24, color=(255, 255, 255)
        ))
        
        y += 60
        self.widgets.append(Label(
            "Difficulty Levels:",
            (width - 200) // 2, y,
            font_size=28, color=(242, 177, 121)
        ))
        
        y += 40
        self.widgets.append(Label(
            "Levels 1-5 (Green): Easy, Target 128",
            80, y,
            font_size=22, color=(143, 240, 164)
        ))
        
        y += 30
        self.widgets.append(Label(
            "Levels 6-10 (Orange): Medium, Target 256",
            80, y,
            font_size=22, color=(242, 177, 121)
        ))
        
        y += 30
        self.widgets.append(Label(
            "Levels 11-15 (Red): Hard, Target 512",
            80, y,
            font_size=22, color=(246, 124, 95)
        ))
        
        y += 30
        self.widgets.append(Label(
            "Levels 16-20 (Dark Red): Expert, Target 1024",
            80, y,
            font_size=22, color=(246, 94, 59)
        ))
        
        self.widgets.append(Button(
            "Back",
            (width - 150) // 2,
            height - 80,
            150, 45,
            callback=self._go_back
        ))
    
    def _go_back(self):
        """Go back to main menu"""
        self.running = False
        self.on_back()
    
    def handle_event(self, event):
        """Handle mouse events"""
        for widget in self.widgets:
            if hasattr(widget, 'handle_event'):
                widget.handle_event(event)
    
    def draw(self, screen):
        """Draw tutorial screen"""
        screen.fill((187, 173, 160))
        
        title_font = pygame.font.Font(None, 56)
        title_surf = title_font.render("Tutorial", True, (255, 255, 255))
        title_rect = title_surf.get_rect(centerx=screen.get_width() // 2, y=40)
        pygame.draw.rect(screen, (242, 177, 121), title_rect.inflate(40, 20))
        screen.blit(title_surf, title_rect)
        
        for widget in self.widgets:
            widget.draw(screen)
    
    def is_running(self):
        """Check if menu is running"""
        return self.running
    
    def reset(self):
        """Reset menu state"""
        self.running = True
