#!/usr/bin/env python3
"""Test cases for ThemeManager"""

from __future__ import print_function

import os
import sys
import json
import tempfile

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.theme_manager import ThemeManager


class TestThemeManager:
    """Test suite for ThemeManager"""

    def __init__(self):
        self.theme_manager = ThemeManager()
        self.test_theme_dir = tempfile.mkdtemp()
        self.test_results = []

    def test_1_initialization(self):
        """Test theme manager initialization"""
        print("\n=== Test 1: Initialization ===")
        try:
            assert self.theme_manager is not None
            assert hasattr(self.theme_manager, 'themes')
            assert hasattr(self.theme_manager, 'current_theme')
            assert 'default' in self.theme_manager.themes
            self.test_results.append(("PASS", "ThemeManager initialized successfully"))
        except AssertionError as e:
            self.test_results.append(("FAIL", f"Initialization failed: {e}"))

    def test_2_get_default_theme(self):
        """Test getting default theme"""
        print("\n=== Test 2: Get Default Theme ===")
        try:
            theme = self.theme_manager.get_theme('default')
            assert theme is not None
            assert 'name' in theme
            assert 'colors' in theme
            assert theme['name'] == 'Default'
            self.test_results.append(("PASS", "Default theme retrieved successfully"))
        except AssertionError as e:
            self.test_results.append(("FAIL", f"Failed to get default theme: {e}"))

    def test_3_apply_theme(self):
        """Test applying a theme"""
        print("\n=== Test 3: Apply Theme ===")
        try:
            self.theme_manager.apply_theme('ocean')
            assert self.theme_manager.current_theme == 'ocean'
            colors = self.theme_manager.get_current_colors()
            assert 'background' in colors
            assert 'grid' in colors
            self.test_results.append(("PASS", "Theme applied successfully"))
        except AssertionError as e:
            self.test_results.append(("FAIL", f"Failed to apply theme: {e}"))

    def test_4_create_custom_theme(self):
        """Test creating a custom theme"""
        print("\n=== Test 4: Create Custom Theme ===")
        try:
            custom_colors = {
                'background': '#1a1a2e',
                'grid': '#16213e',
                'empty': '#0f3460',
                'tile_default': '#e94560',
                'text_dark': '#ffffff',
                'text_light': '#a8b5c0'
            }
            
            success = self.theme_manager.create_theme('test_custom', 'Test Custom', custom_colors)
            assert success
            assert 'test_custom' in self.theme_manager.themes
            self.test_results.append(("PASS", "Custom theme created successfully"))
        except Exception as e:
            self.test_results.append(("FAIL", f"Failed to create custom theme: {e}"))

    def test_5_update_theme(self):
        """Test updating an existing theme"""
        print("\n=== Test 5: Update Theme ===")
        try:
            new_colors = {
                'background': '#2d2d2d',
                'grid': '#3d3d3d'
            }
            
            success = self.theme_manager.update_theme('test_custom', new_colors)
            assert success
            theme = self.theme_manager.get_theme('test_custom')
            assert theme['colors']['background'] == '#2d2d2d'
            assert theme['colors']['grid'] == '#3d3d3d'
            self.test_results.append(("PASS", "Theme updated successfully"))
        except Exception as e:
            self.test_results.append(("FAIL", f"Failed to update theme: {e}"))

    def test_6_delete_theme(self):
        """Test deleting a theme"""
        print("\n=== Test 6: Delete Theme ===")
        try:
            # Create a test theme first
            test_colors = {'background': '#000000', 'grid': '#111111'}
            self.theme_manager.create_theme('to_delete', 'To Delete', test_colors)
            
            success = self.theme_manager.delete_theme('to_delete')
            assert success
            assert 'to_delete' not in self.theme_manager.themes
            self.test_results.append(("PASS", "Theme deleted successfully"))
        except Exception as e:
            self.test_results.append(("FAIL", f"Failed to delete theme: {e}"))

    def test_7_export_theme(self):
        """Test exporting a theme"""
        print("\n=== Test 7: Export Theme ===")
        try:
            export_path = os.path.join(self.test_theme_dir, 'exported_theme.json')
            success = self.theme_manager.export_theme('ocean', export_path)
            
            assert success
            assert os.path.exists(export_path)
            
            with open(export_path, 'r') as f:
                exported_data = json.load(f)
            
            assert exported_data['name'] == 'Ocean'
            assert 'colors' in exported_data
            self.test_results.append(("PASS", "Theme exported successfully"))
        except Exception as e:
            self.test_results.append(("FAIL", f"Failed to export theme: {e}"))

    def test_8_import_theme(self):
        """Test importing a theme"""
        print("\n=== Test 8: Import Theme ===")
        try:
            # Create a test theme file
            import_data = {
                'name': 'Imported Theme',
                'colors': {
                    'background': '#ff0000',
                    'grid': '#00ff00',
                    'empty': '#0000ff',
                    'tile_default': '#ffff00',
                    'text_dark': '#ffffff',
                    'text_light': '#000000'
                }
            }
            
            import_path = os.path.join(self.test_theme_dir, 'import_test.json')
            with open(import_path, 'w') as f:
                json.dump(import_data, f)
            
            success = self.theme_manager.import_theme(import_path)
            assert success
            assert 'imported_theme' in self.theme_manager.themes
            
            imported_theme = self.theme_manager.get_theme('imported_theme')
            assert imported_theme['name'] == 'Imported Theme'
            self.test_results.append(("PASS", "Theme imported successfully"))
        except Exception as e:
            self.test_results.append(("FAIL", f"Failed to import theme: {e}"))

    def test_9_get_preview_colors(self):
        """Test getting preview colors"""
        print("\n=== Test 9: Get Preview Colors ===")
        try:
            preview = self.theme_manager.get_preview_colors('sunset')
            assert preview is not None
            assert 'background' in preview
            assert 'grid' in preview
            assert 'accent' in preview
            assert 'text' in preview
            self.test_results.append(("PASS", "Preview colors retrieved successfully"))
        except Exception as e:
            self.test_results.append(("FAIL", f"Failed to get preview colors: {e}"))

    def test_10_get_theme_names(self):
        """Test getting list of theme names"""
        print("\n=== Test 10: Get Theme Names ===")
        try:
            theme_names = self.theme_manager.get_theme_names()
            assert isinstance(theme_names, list)
            assert len(theme_names) >= 1
            assert 'default' in theme_names
            self.test_results.append(("PASS", "Theme names retrieved successfully"))
        except Exception as e:
            self.test_results.append(("FAIL", f"Failed to get theme names: {e}"))

    def test_11_validate_theme_colors(self):
        """Test validating theme colors"""
        print("\n=== Test 11: Validate Theme Colors ===")
        try:
            # Test valid colors
            valid_colors = {
                'background': '#ffffff',
                'grid': '#cccccc',
                'empty': '#eeeeee'
            }
            assert self.theme_manager._validate_colors(valid_colors)
            
            # Test invalid colors
            invalid_colors = {
                'background': 'not_a_color',
                'grid': '#cccccc'
            }
            assert not self.theme_manager._validate_colors(invalid_colors)
            
            self.test_results.append(("PASS", "Theme colors validated successfully"))
        except Exception as e:
            self.test_results.append(("FAIL", f"Failed to validate theme colors: {e}"))

    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        
        passed = sum(1 for result in self.test_results if result[0] == "PASS")
        failed = sum(1 for result in self.test_results if result[0] == "FAIL")
        
        for status, message in self.test_results:
            print(f"[{status}] {message}")
        
        print("\n" + "="*60)
        print(f"Total: {len(self.test_results)} tests")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {passed/len(self.test_results)*100:.1f}%")
        print("="*60)

        return failed == 0

    def run_all_tests(self):
        """Run all tests"""
        print("Running ThemeManager Test Suite...")
        print("="*60)
        
        self.test_1_initialization()
        self.test_2_get_default_theme()
        self.test_3_apply_theme()
        self.test_4_create_custom_theme()
        self.test_5_update_theme()
        self.test_6_delete_theme()
        self.test_7_export_theme()
        self.test_8_import_theme()
        self.test_9_get_preview_colors()
        self.test_10_get_theme_names()
        self.test_11_validate_theme_colors()
        
        return self.print_summary()


if __name__ == "__main__":
    tester = TestThemeManager()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
