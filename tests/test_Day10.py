import pytest
import sys
import os

# Add parent directory to path to import Day10
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Day10 import parse_line, toggle_lights, find_minimum_presses

class TestParseLine:
    """Test cases for the parse_line function"""
    
    def test_parse_line_basic_single_button(self):
        """Test parsing a line with a single button."""
        line = "[.##.] (3) {3,5,4,7}"
        target_state, buttons = parse_line(line)
        assert target_state == [False, True, True, False]
        assert buttons == [(3,)]
    
    def test_parse_line_multiple_buttons(self):
        """Test parsing a line with multiple buttons."""
        line = "[.##.] (3) (1,3) (2) {3,5,4,7}"
        target_state, buttons = parse_line(line)
        assert target_state == [False, True, True, False]
        assert buttons == [(3,), (1, 3), (2,)]
    
    def test_parse_line_example_one(self):
        """Test first example from problem."""
        line = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
        target_state, buttons = parse_line(line)
        assert target_state == [False, True, True, False]
        assert len(buttons) == 6
        assert buttons == [(3,), (1, 3), (2,), (2, 3), (0, 2), (0, 1)]
    
    def test_parse_line_example_two(self):
        """Test second example from problem."""
        line = "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}"
        target_state, buttons = parse_line(line)
        assert target_state == [False, False, False, True, False]
        assert len(buttons) == 5
        assert (0, 2, 3, 4) in buttons
        assert (2, 3) in buttons
    
    def test_parse_line_example_three(self):
        """Test third example from problem."""
        line = "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"
        target_state, buttons = parse_line(line)
        assert target_state == [False, True, True, True, False, True]
        assert len(buttons) == 4
    
    def test_parse_line_all_off(self):
        """Test parsing a line with all lights off."""
        line = "[....] (1) (2) {1,2}"
        target_state, buttons = parse_line(line)
        assert target_state == [False, False, False, False]
        assert buttons == [(1,), (2,)]
    
    def test_parse_line_all_on(self):
        """Test parsing a line with all lights on."""
        line = "[####] (1) (2) {1,2}"
        target_state, buttons = parse_line(line)
        assert target_state == [True, True, True, True]
        assert buttons == [(1,), (2,)]
    
    def test_parse_line_single_light(self):
        """Test parsing a line with a single light."""
        line = "[#] (0) {1}"
        target_state, buttons = parse_line(line)
        assert target_state == [True]
        assert buttons == [(0,)]
    
    def test_parse_line_ignores_curly_braces(self):
        """Test that curly braces content is ignored."""
        line = "[.##.] (3) (1,3) {999,888,777}"
        target_state, buttons = parse_line(line)
        assert target_state == [False, True, True, False]
        assert buttons == [(3,), (1, 3)]
    
    def test_parse_line_no_curly_braces(self):
        """Test parsing when curly braces are absent."""
        line = "[.##.] (3) (1,3)"
        target_state, buttons = parse_line(line)
        assert target_state == [False, True, True, False]
        assert buttons == [(3,), (1, 3)]
    
    def test_parse_line_whitespace_handling(self):
        """Test that whitespace is handled correctly."""
        line = "  [.##.] (3) (1,3) {3,5}  "
        target_state, buttons = parse_line(line)
        assert target_state == [False, True, True, False]
        assert buttons == [(3,), (1, 3)]

class TestToggleLights:
    """Test cases for the toggle_lights function"""
    
    def test_toggle_lights_single_index(self):
        """Test toggling a single light."""
        state = [False, False, False]
        button = (1,)
        result = toggle_lights(state, button)
        assert result == [False, True, False]
        # Original state should not be modified
        assert state == [False, False, False]
    
    def test_toggle_lights_multiple_indices(self):
        """Test toggling multiple lights."""
        state = [False, False, False, False]
        button = (0, 2, 3)
        result = toggle_lights(state, button)
        assert result == [True, False, True, True]
    
    def test_toggle_lights_toggle_twice(self):
        """Test that toggling twice returns to original state."""
        state = [False, True, False]
        button = (1,)
        result1 = toggle_lights(state, button)
        assert result1 == [False, False, False]
        result2 = toggle_lights(result1, button)
        assert result2 == [False, True, False]
    
    def test_toggle_lights_all_lights(self):
        """Test toggling all lights."""
        state = [False, False, False]
        button = (0, 1, 2)
        result = toggle_lights(state, button)
        assert result == [True, True, True]
    
    def test_toggle_lights_empty_button(self):
        """Test that empty button doesn't change state."""
        state = [False, True, False]
        button = ()
        result = toggle_lights(state, button)
        assert result == [False, True, False]
    
    def test_toggle_lights_out_of_bounds_ignored(self):
        """Test that out-of-bounds indices are ignored."""
        state = [False, True, False]
        button = (0, 5, 1)  # 5 is out of bounds
        result = toggle_lights(state, button)
        assert result == [True, False, False]
    
    def test_toggle_lights_negative_index_ignored(self):
        """Test that negative indices are ignored."""
        state = [False, True, False]
        button = (0, -1, 1)
        result = toggle_lights(state, button)
        # -1 is out of bounds (not in range), so only 0 and 1 toggle
        assert result == [True, False, False]
    
    def test_toggle_lights_duplicate_indices(self):
        """Test that duplicate indices toggle twice (cancel out)."""
        state = [False, True, False]
        button = (1, 1)  # Toggle same index twice
        result = toggle_lights(state, button)
        assert result == [False, True, False]  # Back to original

class TestFindMinimumPresses:
    """Test cases for the find_minimum_presses function"""
    
    def test_find_minimum_presses_example_one(self):
        """Test first example: [.##.] should require 2 presses."""
        target_state = [False, True, True, False]
        buttons = [(3,), (1, 3), (2,), (2, 3), (0, 2), (0, 1)]
        result = find_minimum_presses(target_state, buttons)
        assert result == 2
    
    def test_find_minimum_presses_example_two(self):
        """Test second example: [...#.] should require 3 presses."""
        target_state = [False, False, False, True, False]
        buttons = [(0, 2, 3, 4), (2, 3), (0, 4), (0, 1, 2), (1, 2, 3, 4)]
        result = find_minimum_presses(target_state, buttons)
        assert result == 3
    
    def test_find_minimum_presses_example_three(self):
        """Test third example: [.###.#] should require 2 presses."""
        target_state = [False, True, True, True, False, True]
        buttons = [(0, 1, 2, 3, 4), (0, 3, 4), (0, 1, 2, 4, 5), (1, 2)]
        result = find_minimum_presses(target_state, buttons)
        assert result == 2
    
    def test_find_minimum_presses_already_solved(self):
        """Test that already solved state returns 0."""
        target_state = [False, False, False]
        buttons = [(0,), (1,), (2,)]
        result = find_minimum_presses(target_state, buttons)
        assert result == 0
    
    def test_find_minimum_presses_single_button_solution(self):
        """Test case where single button solves it."""
        target_state = [True, False, False]
        buttons = [(0,), (1,), (2,)]
        result = find_minimum_presses(target_state, buttons)
        assert result == 1
    
    def test_find_minimum_presses_single_light(self):
        """Test with a single light."""
        target_state = [True]
        buttons = [(0,)]
        result = find_minimum_presses(target_state, buttons)
        assert result == 1
    
    def test_find_minimum_presses_single_light_off(self):
        """Test with a single light that should be off."""
        target_state = [False]
        buttons = [(0,)]
        result = find_minimum_presses(target_state, buttons)
        assert result == 0
    
    def test_find_minimum_presses_two_button_combination(self):
        """Test case requiring two specific buttons."""
        target_state = [True, True, False]
        buttons = [(0,), (1,), (0, 1)]
        # Pressing (0,1) once gives [True, True, False] from [False, False, False] = 1 press
        result = find_minimum_presses(target_state, buttons)
        assert result == 1
    
    def test_find_minimum_presses_all_on(self):
        """Test turning all lights on."""
        target_state = [True, True, True]
        buttons = [(0,), (1,), (2,)]
        result = find_minimum_presses(target_state, buttons)
        assert result == 3
    
    def test_find_minimum_presses_complex_pattern(self):
        """Test a more complex pattern."""
        target_state = [True, False, True, False, True]
        buttons = [(0,), (2,), (4,)]
        result = find_minimum_presses(target_state, buttons)
        assert result == 3
    
    def test_find_minimum_presses_button_combination(self):
        """Test that button combinations work correctly."""
        target_state = [True, True, False]
        # Buttons: (0,1) toggles both 0 and 1
        # To get [True, True, False], we can press (0,1) once
        buttons = [(0, 1), (2,)]
        result = find_minimum_presses(target_state, buttons)
        assert result == 1
    
    def test_find_minimum_presses_impossible_case(self):
        """Test case that might be impossible (though unlikely with toggle)."""
        # With toggle operations, most states should be reachable
        # But let's test with a very constrained set
        target_state = [True, False]
        buttons = [(0,)]  # Can only toggle first light
        result = find_minimum_presses(target_state, buttons)
        assert result == 1  # Should be possible
    
    def test_find_minimum_presses_empty_buttons(self):
        """Test with empty button list."""
        target_state = [True, False]
        buttons = []
        result = find_minimum_presses(target_state, buttons)
        # Can't reach target from all-off without buttons
        assert result == -1
    
    def test_find_minimum_presses_large_state(self):
        """Test with a larger state space."""
        target_state = [True, False, True, False, True, False]
        buttons = [(0,), (1,), (2,), (3,), (4,), (5,)]
        result = find_minimum_presses(target_state, buttons)
        assert result == 3  # Need to toggle indices 0, 2, 4

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

