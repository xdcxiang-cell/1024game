#!/usr/bin/env python3
"""Test cases for TutorialManager"""

from __future__ import print_function

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.tutorial_manager import TutorialManager


class TestTutorialManager:
    """Test suite for TutorialManager"""

    def __init__(self):
        self.tutorial_manager = TutorialManager()
        self.test_results = []

    def test_1_initialization(self):
        """Test tutorial manager initialization"""
        print("\n=== Test 1: Initialization ===")
        try:
            assert self.tutorial_manager is not None
            assert hasattr(self.tutorial_manager, 'tutorials')
            assert hasattr(self.tutorial_manager, 'progress')
            assert len(self.tutorial_manager.tutorials) >= 3
            self.test_results.append(("PASS", "TutorialManager initialized successfully"))
        except AssertionError as e:
            self.test_results.append(("FAIL", f"Initialization failed: {e}"))

    def test_2_get_all_tutorials(self):
        """Test getting all tutorials"""
        print("\n=== Test 2: Get All Tutorials ===")
        try:
            tutorials = self.tutorial_manager.get_all_tutorials()
            assert isinstance(tutorials, list)
            assert len(tutorials) >= 3
            
            # Check each tutorial has required fields
            for tutorial in tutorials:
                assert 'id' in tutorial
                assert 'title' in tutorial
                assert 'description' in tutorial
                assert 'chapters' in tutorial
            
            self.test_results.append(("PASS", "All tutorials retrieved successfully"))
        except AssertionError as e:
            self.test_results.append(("FAIL", f"Failed to get tutorials: {e}"))

    def test_3_get_tutorial(self):
        """Test getting a specific tutorial"""
        print("\n=== Test 3: Get Specific Tutorial ===")
        try:
            tutorial = self.tutorial_manager.get_tutorial('basics')
            assert tutorial is not None
            assert tutorial['id'] == 'basics'
            assert tutorial['title'] == '基础游戏玩法'
            assert 'chapters' in tutorial
            assert len(tutorial['chapters']) > 0
            
            self.test_results.append(("PASS", "Specific tutorial retrieved successfully"))
        except AssertionError as e:
            self.test_results.append(("FAIL", f"Failed to get tutorial: {e}"))

    def test_4_get_tutorial_chapters(self):
        """Test getting tutorial chapters"""
        print("\n=== Test 4: Get Tutorial Chapters ===")
        try:
            chapters = self.tutorial_manager.get_tutorial_chapters('advanced')
            assert isinstance(chapters, list)
            assert len(chapters) > 0
            
            # Check chapter structure
            for chapter in chapters:
                assert 'id' in chapter
                assert 'title' in chapter
                assert 'content' in chapter
            
            self.test_results.append(("PASS", "Tutorial chapters retrieved successfully"))
        except AssertionError as e:
            self.test_results.append(("FAIL", f"Failed to get chapters: {e}"))

    def test_5_mark_chapter_completed(self):
        """Test marking a chapter as completed"""
        print("\n=== Test 5: Mark Chapter Completed ===")
        try:
            # Get first chapter of basics tutorial
            chapters = self.tutorial_manager.get_tutorial_chapters('basics')
            first_chapter_id = chapters[0]['id']
            
            # Mark as completed
            self.tutorial_manager.mark_chapter_completed('basics', first_chapter_id)
            
            # Verify
            progress = self.tutorial_manager.progress.get('basics', {})
            assert first_chapter_id in progress.get('completed_chapters', [])
            
            self.test_results.append(("PASS", "Chapter marked as completed"))
        except AssertionError as e:
            self.test_results.append(("FAIL", f"Failed to mark chapter: {e}"))

    def test_6_get_completion_percentage(self):
        """Test getting tutorial completion percentage"""
        print("\n=== Test 6: Get Completion Percentage ===")
        try:
            # Should be > 0 since we marked a chapter in test 5
            percentage = self.tutorial_manager.get_completion_percentage('basics')
            assert isinstance(percentage, int)
            assert percentage >= 0
            assert percentage <= 100
            assert percentage > 0
            
            self.test_results.append(("PASS", f"Completion percentage calculated: {percentage}%"))
        except AssertionError as e:
            self.test_results.append(("FAIL", f"Failed to calculate percentage: {e}"))

    def test_7_is_tutorial_completed(self):
        """Test checking if tutorial is completed"""
        print("\n=== Test 7: Is Tutorial Completed ===")
        try:
            # Should not be completed yet
            is_completed = self.tutorial_manager.is_tutorial_completed('basics')
            assert is_completed is False
            
            # Mark all chapters as completed
            chapters = self.tutorial_manager.get_tutorial_chapters('basics')
            for chapter in chapters:
                self.tutorial_manager.mark_chapter_completed('basics', chapter['id'])
            
            # Now should be completed
            is_completed = self.tutorial_manager.is_tutorial_completed('basics')
            assert is_completed is True
            
            self.test_results.append(("PASS", "Tutorial completion status checked correctly"))
        except AssertionError as e:
            self.test_results.append(("FAIL", f"Failed to check completion: {e}"))

    def test_8_mark_tutorial_completed(self):
        """Test marking entire tutorial as completed"""
        print("\n=== Test 8: Mark Tutorial Completed ===")
        try:
            # Mark tutorial as completed
            self.tutorial_manager.mark_tutorial_completed('strategy')
            
            # Verify
            progress = self.tutorial_manager.progress.get('strategy', {})
            assert progress.get('completed', False) is True
            
            self.test_results.append(("PASS", "Tutorial marked as completed"))
        except AssertionError as e:
            self.test_results.append(("FAIL", f"Failed to mark tutorial: {e}"))

    def test_9_get_completed_chapters(self):
        """Test getting completed chapters"""
        print("\n=== Test 9: Get Completed Chapters ===")
        try:
            # Get completed chapters for basics
            completed = self.tutorial_manager.get_completed_chapters('basics')
            assert isinstance(completed, list)
            
            # Get tutorial chapters
            chapters = self.tutorial_manager.get_tutorial_chapters('basics')
            
            # Should have all chapters marked as completed
            assert len(completed) == len(chapters)
            
            self.test_results.append(("PASS", f"Completed chapters retrieved: {len(completed)} chapters"))
        except AssertionError as e:
            self.test_results.append(("FAIL", f"Failed to get completed chapters: {e}"))

    def test_10_reset_progress(self):
        """Test resetting tutorial progress"""
        print("\n=== Test 10: Reset Progress ===")
        try:
            # Reset progress for basics
            self.tutorial_manager.reset_progress('basics')
            
            # Verify
            is_completed = self.tutorial_manager.is_tutorial_completed('basics')
            assert is_completed is False
            
            completed = self.tutorial_manager.get_completed_chapters('basics')
            assert len(completed) == 0
            
            self.test_results.append(("PASS", "Tutorial progress reset successfully"))
        except AssertionError as e:
            self.test_results.append(("FAIL", f"Failed to reset progress: {e}"))

    def test_11_invalid_tutorial_id(self):
        """Test handling invalid tutorial ID"""
        print("\n=== Test 11: Invalid Tutorial ID ===")
        try:
            # Should return None for invalid ID
            tutorial = self.tutorial_manager.get_tutorial('invalid_id')
            assert tutorial is None
            
            # Should return empty list for chapters
            chapters = self.tutorial_manager.get_tutorial_chapters('invalid_id')
            assert chapters == []
            
            # Should return 0% for completion
            percentage = self.tutorial_manager.get_completion_percentage('invalid_id')
            assert percentage == 0
            
            self.test_results.append(("PASS", "Invalid tutorial ID handled correctly"))
        except AssertionError as e:
            self.test_results.append(("FAIL", f"Failed to handle invalid ID: {e}"))

    def test_12_tutorial_structure(self):
        """Test tutorial data structure"""
        print("\n=== Test 12: Tutorial Structure ===")
        try:
            tutorials = self.tutorial_manager.get_all_tutorials()
            
            for tutorial in tutorials:
                # Check tutorial level fields
                assert 'difficulty' in tutorial
                assert 'estimated_time' in tutorial
                
                # Check chapter level fields
                for chapter in tutorial['chapters']:
                    assert 'id' in chapter
                    assert 'title' in chapter
                    assert 'content' in chapter
                    assert isinstance(chapter['content'], list)
                    
                    # Optional fields
                    if 'tip' in chapter:
                        assert isinstance(chapter['tip'], str)
            
            self.test_results.append(("PASS", "All tutorials have correct structure"))
        except AssertionError as e:
            self.test_results.append(("FAIL", f"Tutorial structure validation failed: {e}"))

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
        print("Running TutorialManager Test Suite...")
        print("="*60)
        
        self.test_1_initialization()
        self.test_2_get_all_tutorials()
        self.test_3_get_tutorial()
        self.test_4_get_tutorial_chapters()
        self.test_5_mark_chapter_completed()
        self.test_6_get_completion_percentage()
        self.test_7_is_tutorial_completed()
        self.test_8_mark_tutorial_completed()
        self.test_9_get_completed_chapters()
        self.test_10_reset_progress()
        self.test_11_invalid_tutorial_id()
        self.test_12_tutorial_structure()
        
        return self.print_summary()


if __name__ == "__main__":
    tester = TestTutorialManager()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
