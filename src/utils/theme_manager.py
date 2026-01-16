#!/usr/bin/env python3
"""Theme Manager - Handles theme customization and persistence"""

import json
import os
from typing import Dict, Optional
from pathlib import Path

from src.engine.constants import COLORS, TILE_VALUES


class ThemeManager:
    """Manages theme customization and application"""

    def __init__(self, themes_dir: str = 'themes'):
        self.themes_dir = themes_dir
        self._ensure_directory()
        self.themes = self._load_all_themes()
        self.current_theme = None

    def _ensure_directory(self):
        """Ensure themes directory exists"""
        os.makedirs(self.themes_dir, exist_ok=True)

    def _load_all_themes(self) -> Dict:
        """Load all themes from themes directory"""
        themes = {}
        
        # Add default theme
        themes['default'] = self._get_default_theme()
        
        # Load custom themes from JSON files
        if os.path.exists(self.themes_dir):
            for filename in os.listdir(self.themes_dir):
                if filename.endswith('.json'):
                    theme_name = os.path.splitext(filename)[0]
                    try:
                        filepath = os.path.join(self.themes_dir, filename)
                        with open(filepath, 'r') as f:
                            theme_data = json.load(f)
                            themes[theme_name] = theme_data
                    except Exception as e:
                        print(f"Failed to load theme {theme_name}: {e}")
        
        return themes

    def _get_default_theme(self) -> Dict:
        """Get default theme definition"""
        return {
            'name': 'Default',
            'author': 'System',
            'version': '1.0',
            'colors': COLORS.copy(),
            'tile_values': TILE_VALUES.copy()
        }

    def get_theme(self, theme_name: str) -> Optional[Dict]:
        """Get theme by name"""
        return self.themes.get(theme_name)

    def get_theme_names(self) -> list:
        """Get list of available theme names"""
        return list(self.themes.keys())

    def apply_theme(self, theme_name: str) -> bool:
        """Apply a theme to the game"""
        if theme_name not in self.themes:
            print(f"Theme '{theme_name}' not found")
            return False
        
        self.current_theme = theme_name
        theme = self.themes[theme_name]
        
        # Update COLORS with theme colors
        if 'colors' in theme:
            COLORS.update(theme['colors'])
        
        # Update TILE_VALUES with theme tile values
        if 'tile_values' in theme:
            TILE_VALUES.update(theme['tile_values'])
        
        print(f"Applied theme: {theme_name}")
        return True

    def create_theme(self, theme_name: str, colors: Dict, tile_values: Optional[Dict] = None, 
                    author: str = 'User') -> bool:
        """Create a new custom theme"""
        if theme_name in self.themes:
            print(f"Theme '{theme_name}' already exists")
            return False
        
        theme = {
            'name': theme_name,
            'author': author,
            'version': '1.0',
            'colors': colors,
            'tile_values': tile_values or TILE_VALUES.copy()
        }
        
        # Save theme to JSON file
        filepath = os.path.join(self.themes_dir, f'{theme_name}.json')
        try:
            with open(filepath, 'w') as f:
                json.dump(theme, f, indent=2)
            
            self.themes[theme_name] = theme
            print(f"Created theme: {theme_name}")
            return True
        except Exception as e:
            print(f"Failed to create theme {theme_name}: {e}")
            return False

    def update_theme(self, theme_name: str, colors: Optional[Dict] = None, 
                    tile_values: Optional[Dict] = None) -> bool:
        """Update an existing theme"""
        if theme_name not in self.themes:
            print(f"Theme '{theme_name}' not found")
            return False
        
        theme = self.themes[theme_name]
        
        if colors:
            theme['colors'].update(colors)
        
        if tile_values:
            theme['tile_values'].update(tile_values)
        
        # Save updated theme
        filepath = os.path.join(self.themes_dir, f'{theme_name}.json')
        try:
            with open(filepath, 'w') as f:
                json.dump(theme, f, indent=2)
            
            print(f"Updated theme: {theme_name}")
            return True
        except Exception as e:
            print(f"Failed to update theme {theme_name}: {e}")
            return False

    def delete_theme(self, theme_name: str) -> bool:
        """Delete a custom theme"""
        if theme_name == 'default':
            print("Cannot delete default theme")
            return False
        
        if theme_name not in self.themes:
            print(f"Theme '{theme_name}' not found")
            return False
        
        filepath = os.path.join(self.themes_dir, f'{theme_name}.json')
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                del self.themes[theme_name]
                
                # If deleting current theme, revert to default
                if self.current_theme == theme_name:
                    self.apply_theme('default')
                
                print(f"Deleted theme: {theme_name}")
                return True
            except Exception as e:
                print(f"Failed to delete theme {theme_name}: {e}")
                return False
        
        return False

    def export_theme(self, theme_name: str, export_path: str) -> bool:
        """Export theme to file"""
        if theme_name not in self.themes:
            print(f"Theme '{theme_name}' not found")
            return False
        
        theme = self.themes[theme_name]
        
        try:
            with open(export_path, 'w') as f:
                json.dump(theme, f, indent=2)
            
            print(f"Exported theme '{theme_name}' to {export_path}")
            return True
        except Exception as e:
            print(f"Failed to export theme {theme_name}: {e}")
            return False

    def import_theme(self, import_path: str, theme_name: Optional[str] = None) -> bool:
        """Import theme from file"""
        if not os.path.exists(import_path):
            print(f"File '{import_path}' not found")
            return False
        
        try:
            with open(import_path, 'r') as f:
                theme = json.load(f)
            
            if not theme_name:
                theme_name = theme.get('name', os.path.splitext(os.path.basename(import_path))[0])
            
            # Save imported theme
            filepath = os.path.join(self.themes_dir, f'{theme_name}.json')
            with open(filepath, 'w') as f:
                json.dump(theme, f, indent=2)
            
            self.themes[theme_name] = theme
            print(f"Imported theme: {theme_name}")
            return True
        except Exception as e:
            print(f"Failed to import theme: {e}")
            return False

    def get_preview_colors(self, theme_name: str) -> Dict:
        """Get preview colors for a theme"""
        theme = self.get_theme(theme_name)
        if not theme:
            return {}
        
        colors = theme.get('colors', {})
        return {
            'background': colors.get('background', '#faf8ef'),
            'grid': colors.get('grid', '#bbada0'),
            'accent': colors.get('accent', '#8f7a66'),
            'text': colors.get('text_dark', '#776e65')
        }
    def get_current_colors(self) -> Dict:
        """Get current colors dictionary"""
        from src.engine.constants import COLORS
        return COLORS

    def validate_theme(self, theme: Dict) -> bool:
        """Validate theme structure"""
        if 'name' not in theme:
            return False
        
        if 'colors' not in theme:
            return False
        
        # Check required color keys
        required_colors = ['background', 'grid', 'empty', 'text_light', 'text_dark']
        for color_key in required_colors:
            if color_key not in theme['colors']:
                return False
        
        return True

    def duplicate_theme(self, source_name: str, new_name: str) -> bool:
        """Duplicate an existing theme"""
        if source_name not in self.themes:
            print(f"Theme '{source_name}' not found")
            return False
        
        if new_name in self.themes:
            print(f"Theme '{new_name}' already exists")
            return False
        
        source_theme = self.themes[source_name]
        new_theme = {
            'name': new_name,
            'author': source_theme.get('author', 'User'),
            'version': source_theme.get('version', '1.0'),
            'colors': source_theme['colors'].copy(),
            'tile_values': source_theme['tile_values'].copy()
        }
        
        self.themes[new_name] = new_theme
        
        filepath = os.path.join(self.themes_dir, f'{new_name}.json')
        try:
            with open(filepath, 'w') as f:
                json.dump(new_theme, f, indent=2)
            
            print(f"Duplicated theme '{source_name}' as '{new_name}'")
            return True
        except Exception as e:
            print(f"Failed to duplicate theme: {e}")
            return False
