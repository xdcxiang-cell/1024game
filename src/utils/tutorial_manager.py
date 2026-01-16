#!/usr/bin/env python3
"""Tutorial Manager - Handles game tutorial system"""

import json
import os
from typing import Dict, List, Optional


class TutorialManager:
    """Manages tutorial system and player progress"""

    def __init__(self, tutorial_dir: str = 'tutorials'):
        self.tutorial_dir = tutorial_dir
        self._ensure_directory()
        self.tutorials = self._load_all_tutorials()
        self.player_progress = self._load_player_progress()

    def _ensure_directory(self):
        """Ensure tutorial directory exists"""
        os.makedirs(self.tutorial_dir, exist_ok=True)

    def _load_all_tutorials(self) -> Dict:
        """Load all tutorials from JSON files"""
        tutorials = {}
        
        # Add built-in tutorials
        tutorials['basic'] = self._get_basic_tutorial()
        tutorials['advanced'] = self._get_advanced_tutorial()
        tutorials['strategy'] = self._get_strategy_tutorial()
        
        # Load custom tutorials from JSON files
        if os.path.exists(self.tutorial_dir):
            for filename in os.listdir(self.tutorial_dir):
                if filename.endswith('.json'):
                    tutorial_name = os.path.splitext(filename)[0]
                    try:
                        filepath = os.path.join(self.tutorial_dir, filename)
                        with open(filepath, 'r') as f:
                            tutorial_data = json.load(f)
                            tutorials[tutorial_name] = tutorial_data
                    except Exception as e:
                        print(f"Failed to load tutorial {tutorial_name}: {e}")
        
        return tutorials

    def _get_basic_tutorial(self) -> Dict:
        """Get basic tutorial content"""
        return {
            'id': 'basic',
            'title': 'Basic Gameplay',
            'description': 'Learn the fundamental mechanics of 2048',
            'difficulty': 'beginner',
            'estimated_time': '5 minutes',
            'chapters': [
                {
                    'id': 'ch1',
                    'title': 'Welcome to 2048',
                    'content': [
                        "Welcome to the 2048 number puzzle game!",
                        "Your goal is to slide tiles on a 4x4 grid and merge them to reach the 2048 tile.",
                        "Use the arrow keys (↑↓←→) or WASD keys to move all tiles in the selected direction."
                    ],
                    'image': None,
                    'tip': 'Start by exploring the controls and getting comfortable with movement.'
                },
                {
                    'id': 'ch2',
                    'title': 'Tile Movement',
                    'content': [
                        "When you press a direction key, ALL tiles move as far as possible in that direction.",
                        "Tiles will stop when they hit another tile or the edge of the grid.",
                        "Try moving tiles in different directions to see how they behave."
                    ],
                    'image': None,
                    'tip': 'Practice moving in all directions to understand the mechanics.'
                },
                {
                    'id': 'ch3',
                    'title': 'Tile Merging',
                    'content': [
                        "The key to 2048 is merging tiles!",
                        "When two tiles with the SAME NUMBER touch, they merge into one.",
                        "For example: 2 + 2 = 4, 4 + 4 = 8, and so on...",
                        "Each merge creates a tile with double the value.",
                        "Merging tiles also earns you points!"
                    ],
                    'image': None,
                    'tip': 'Look for opportunities to merge tiles strategically.'
                },
                {
                    'id': 'ch4',
                    'title': 'New Tile Spawning',
                    'content': [
                        "After each valid move, a new tile appears on the grid.",
                        "New tiles are usually 2s, but occasionally they can be 4s.",
                        "Tiles appear in empty spaces randomly."
                    ],
                    'image': None,
                    'tip': 'Plan your moves considering where new tiles might appear.'
                },
                {
                    'id': 'ch5',
                    'title': 'Winning the Game',
                    'content': [
                        "The primary goal is to create a 2048 tile!",
                        "But don't stop there - see how high you can go!",
                        "Players have reached tile values like 4096, 8192, and even higher.",
                        "The game continues after reaching 2048, so keep challenging yourself!"
                    ],
                    'image': None,
                    'tip': "Remember: the game doesn't end at 2048. Aim for higher scores!"
                }
            ]
        }

    def _get_advanced_tutorial(self) -> Dict:
        """Get advanced tutorial content"""
        return {
            'id': 'advanced',
            'title': 'Advanced Techniques',
            'description': 'Master advanced strategies for higher scores',
            'difficulty': 'intermediate',
            'estimated_time': '8 minutes',
            'chapters': [
                {
                    'id': 'adv1',
                    'title': 'Corner Strategy',
                    'content': [
                        "The corner strategy is one of the most effective techniques.",
                        "Keep your largest tile in one corner of the grid.",
                        "Use the adjacent edge to build up tiles before merging.",
                        "This prevents your high-value tile from getting trapped."
                    ],
                    'image': None,
                    'tip': 'Choose a corner and stick with it throughout the game.'
                },
                {
                    'id': 'adv2',
                    'title': 'Order Maintenance',
                    'content': [
                        "Try to keep tiles in descending order from the corner.",
                        "For example: 1024 in the corner, then 512, 256, 128, etc.",
                        "This creates a clear path for merging.",
                        "Avoid having high-value tiles scattered across the grid."
                    ],
                    'image': None,
                    'tip': 'Maintaining order prevents difficult situations.'
                },
                {
                    'id': 'adv3',
                    'title': 'Minimizing Movement',
                    'content': [
                        "Every move adds a new tile to the board.",
                        "Try to make moves that serve multiple purposes:",
                        "  - Create merges",
                        "  - Position tiles for future merges",
                        "  - Maintain open spaces",
                        "Avoid moves that just shuffle tiles without purpose."
                    ],
                    'image': None,
                    'tip': 'Think 2-3 moves ahead when planning your strategy.'
                },
                {
                    'id': 'adv4',
                    'title': 'Avoiding Small Corners',
                    'content': [
                        "Be careful about creating small isolated corners with low-value tiles.",
                        "These can trap larger tiles or block movement paths.",
                        "Keep your board as open as possible."
                    ],
                    'image': None,
                    'tip': 'Look for opportunities to consolidate tiles.'
                },
                {
                    'id': 'adv5',
                    'title': 'Undo Feature',
                    'content': [
                        "If you make a move you regret, use the undo feature if available.",
                        "But don't rely on undo too much - it's better to plan ahead.",
                        "Think of each move as a commitment.",
                        "Save undo for critical mistakes, not every minor inconvenience."
                    ],
                    'image': None,
                    'tip': "Practice makes perfect! The more you play, the better you'll get."
                }
            ]
        }

    def _get_strategy_tutorial(self) -> Dict:
        """Get strategy tutorial content"""
        return {
            'id': 'strategy',
            'title': 'Game Strategy',
            'description': 'Develop winning strategies for different game situations',
            'difficulty': 'advanced',
            'estimated_time': '10 minutes',
            'chapters': [
                {
                    'id': 'strat1',
                    'title': 'Early Game Strategy',
                    'content': [
                        "In the early game, focus on building up tile values.",
                        "Don't worry too much about positioning yet - explore and learn.",
                        "Try to create a few 128 or 256 tiles.",
                        "Start identifying which corner you want to use as your main base.",
                        "The goal is to create a foundation for larger merges."
                    ],
                    'image': None,
                    'tip': 'Use this phase to experiment and learn.'
                },
                {
                    'id': 'strat2',
                    'title': 'Mid Game Strategy',
                    'content': [
                        "Once you have 512+ tiles, switch to corner strategy.",
                        "Begin organizing tiles in descending order from your corner.",
                        "Start making more deliberate, thoughtful moves.",
                        "Avoid moves that disrupt your organization.",
                        "Keep the opposite side of the grid relatively clear."
                    ],
                    'image': None,
                    'tip': 'This is where good habits really pay off.'
                },
                {
                    'id': 'strat3',
                    'title': 'End Game Strategy',
                    'content': [
                        "When the board fills up, you need to be very careful.",
                        "Prioritize moves that keep open spaces.",
                        "Be prepared to abandon your corner if necessary to survive.",
                        "Look for 'double moves' that create two merges at once.",
                        "Consider all possible moves before committing."
                    ],
                    'image': None,
                    'tip': 'Stay calm and think through each move carefully.'
                },
                {
                    'id': 'strat4',
                    'title': 'Scoring System',
                    'content': [
                        "Each merge adds points equal to the new tile value.",
                        "For example: 2+2=4 earns 4 points, 1024+1024=2048 earns 2048 points.",
                        "Higher merges are much more valuable.",
                        "A single 2048 merge is worth as much as FIVE HUNDRED 2 merges!",
                        "Focus on creating higher-value tiles for maximum scores."
                    ],
                    'image': None,
                    'tip': 'Quality over quantity - one big merge beats many small ones.'
                },
                {
                    'id': 'strat5',
                    'title': 'Common Mistakes to Avoid',
                    'content': [
                        "1. DON'T move randomly - have a plan",
                        "2. DON'T let high-value tiles get trapped",
                        "3. DON'T fill the entire board unnecessarily",
                        "4. DON'T ignore the opposite side of the grid",
                        "5. DON'T give up! Even losing positions can be turned around.",
                        "The best way to improve is to learn from each game."
                    ],
                    'image': None,
                    'tip': 'Review your games and think about what you could have done differently.'
                }
            ]
        }

    def _load_player_progress(self) -> Dict:
        """Load player's tutorial progress"""
        progress_file = os.path.join(self.tutorial_dir, 'player_progress.json')
        
        if os.path.exists(progress_file):
            try:
                with open(progress_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Failed to load tutorial progress: {e}")
                return {}
        
        return {}

    def _save_player_progress(self):
        """Save player's tutorial progress"""
        progress_file = os.path.join(self.tutorial_dir, 'player_progress.json')
        
        try:
            with open(progress_file, 'w') as f:
                json.dump(self.player_progress, f, indent=2)
            return True
        except Exception as e:
            print(f"Failed to save tutorial progress: {e}")
            return False

    def get_tutorial(self, tutorial_id: str) -> Optional[Dict]:
        """Get tutorial by ID"""
        return self.tutorials.get(tutorial_id)

    def get_all_tutorials(self) -> List[Dict]:
        """Get list of all available tutorials"""
        return list(self.tutorials.values())

    def get_tutorial_chapters(self, tutorial_id: str) -> List[Dict]:
        """Get chapters for a specific tutorial"""
        tutorial = self.get_tutorial(tutorial_id)
        if tutorial:
            return tutorial.get('chapters', [])
        return []

    def get_chapter(self, tutorial_id: str, chapter_id: str) -> Optional[Dict]:
        """Get specific chapter from tutorial"""
        chapters = self.get_tutorial_chapters(tutorial_id)
        for chapter in chapters:
            if chapter['id'] == chapter_id:
                return chapter
        return None

    def mark_chapter_completed(self, tutorial_id: str, chapter_id: str) -> bool:
        """Mark a chapter as completed"""
        if tutorial_id not in self.player_progress:
            self.player_progress[tutorial_id] = {}
        
        self.player_progress[tutorial_id][chapter_id] = True
        return self._save_player_progress()

    def mark_tutorial_completed(self, tutorial_id: str) -> bool:
        """Mark entire tutorial as completed"""
        self.player_progress[f'{tutorial_id}_completed'] = True
        return self._save_player_progress()

    def is_chapter_completed(self, tutorial_id: str, chapter_id: str) -> bool:
        """Check if chapter is completed"""
        tutorial_progress = self.player_progress.get(tutorial_id, {})
        return tutorial_progress.get(chapter_id, False)

    def is_tutorial_completed(self, tutorial_id: str) -> bool:
        """Check if entire tutorial is completed"""
        return self.player_progress.get(f'{tutorial_id}_completed', False)

    def get_completion_percentage(self, tutorial_id: str) -> int:
        """Get completion percentage for tutorial"""
        chapters = self.get_tutorial_chapters(tutorial_id)
        if not chapters:
            return 0
        
        completed = sum(1 for chapter in chapters if self.is_chapter_completed(tutorial_id, chapter['id']))
        return int((completed / len(chapters)) * 100)

    def reset_tutorial_progress(self, tutorial_id: str = None) -> bool:
        """Reset tutorial progress"""
        if tutorial_id:
            # Reset specific tutorial
            if tutorial_id in self.player_progress:
                del self.player_progress[tutorial_id]
            if f'{tutorial_id}_completed' in self.player_progress:
                del self.player_progress[f'{tutorial_id}_completed']
        else:
            # Reset all progress
            self.player_progress.clear()
        
        return self._save_player_progress()

    def get_recommended_tutorial(self) -> Optional[str]:
        """Get recommended tutorial for player"""
        # Check if any tutorials are completed
        if not self.is_tutorial_completed('basic'):
            return 'basic'
        elif not self.is_tutorial_completed('advanced'):
            return 'advanced'
        elif not self.is_tutorial_completed('strategy'):
            return 'strategy'
        else:
            # All tutorials completed, recommend review
            return 'basic'

    def create_tutorial(self, tutorial_data: Dict) -> bool:
        """Create a new custom tutorial"""
        tutorial_id = tutorial_data.get('id')
        
        if not tutorial_id:
            print("Tutorial must have an ID")
            return False
        
        if tutorial_id in self.tutorials:
            print(f"Tutorial '{tutorial_id}' already exists")
            return False
        
        self.tutorials[tutorial_id] = tutorial_data
        
        # Save to file
        filepath = os.path.join(self.tutorial_dir, f'{tutorial_id}.json')
        try:
            with open(filepath, 'w') as f:
                json.dump(tutorial_data, f, indent=2)
            
            print(f"Created tutorial: {tutorial_id}")
            return True
        except Exception as e:
            print(f"Failed to create tutorial {tutorial_id}: {e}")
            return False

    def delete_tutorial(self, tutorial_id: str) -> bool:
        """Delete a tutorial"""
        # Cannot delete built-in tutorials
        if tutorial_id in ['basic', 'advanced', 'strategy']:
            print("Cannot delete built-in tutorials")
            return False
        
        if tutorial_id not in self.tutorials:
            print(f"Tutorial '{tutorial_id}' not found")
            return False
        
        filepath = os.path.join(self.tutorial_dir, f'{tutorial_id}.json')
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                del self.tutorials[tutorial_id]
                print(f"Deleted tutorial: {tutorial_id}")
                return True
            except Exception as e:
                print(f"Failed to delete tutorial {tutorial_id}: {e}")
                return False
        
        return False

    def get_next_chapter(self, tutorial_id: str, current_chapter_id: str) -> Optional[Dict]:
        """Get next chapter in sequence"""
        chapters = self.get_tutorial_chapters(tutorial_id)
        for i, chapter in enumerate(chapters):
            if chapter['id'] == current_chapter_id and i < len(chapters) - 1:
                return chapters[i + 1]
        return None

    def get_previous_chapter(self, tutorial_id: str, current_chapter_id: str) -> Optional[Dict]:
        """Get previous chapter in sequence"""
        chapters = self.get_tutorial_chapters(tutorial_id)
        for i, chapter in enumerate(chapters):
            if chapter['id'] == current_chapter_id and i > 0:
                return chapters[i - 1]
        return None

    def get_progress_summary(self) -> Dict:
        """Get summary of tutorial progress"""
        summary = {
            'tutorials': {},
            'total_completed': 0,
            'total_tutorials': len(self.tutorials)
        }
        
        for tutorial_id, tutorial in self.tutorials.items():
            chapters = tutorial.get('chapters', [])
            completed = sum(1 for chapter in chapters if self.is_chapter_completed(tutorial_id, chapter['id']))
            
            summary['tutorials'][tutorial_id] = {
                'title': tutorial.get('title'),
                'chapters_total': len(chapters),
                'chapters_completed': completed,
                'percentage': int((completed / len(chapters)) * 100) if chapters else 0,
                'completed': self.is_tutorial_completed(tutorial_id)
            }
            
            if self.is_tutorial_completed(tutorial_id):
                summary['total_completed'] += 1
        
        return summary
