import pytest
import sys
import os

# Add parent directory to path to import Day7
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Day7 import add_line_to_grid, build_grid, Cell, CellType, Beam, generate_beams_from_starters, process_beams, Grid

class TestAddLineToGrid:
    def test_add_line_to_grid_one_line(self):
        """Test adding a single line to the grid."""
        grid = []
        add_line_to_grid(grid, "abc")
        
        assert len(grid) == 1
        assert len(grid[0]) == 3
        assert grid[0][0].character == 'a'
        assert grid[0][1].character == 'b'
        assert grid[0][2].character == 'c'
        assert all(isinstance(cell, Cell) for cell in grid[0])
    
    def test_add_line_to_grid_one_line_with_newline(self):
        """Test adding a line with newline character (should be stripped)."""
        grid = []
        add_line_to_grid(grid, "xyz\n")
        
        assert len(grid) == 1
        assert len(grid[0]) == 3
        assert grid[0][0].character == 'x'
        assert grid[0][1].character == 'y'
        assert grid[0][2].character == 'z'
        assert all(isinstance(cell, Cell) for cell in grid[0])
    
    def test_add_line_to_grid_multiple_lines(self):
        """Test adding multiple lines to the grid."""
        grid = []
        add_line_to_grid(grid, "abc")
        add_line_to_grid(grid, "def")
        add_line_to_grid(grid, "ghi")
        
        assert len(grid) == 3
        assert [cell.character for cell in grid[0]] == ['a', 'b', 'c']
        assert [cell.character for cell in grid[1]] == ['d', 'e', 'f']
        assert [cell.character for cell in grid[2]] == ['g', 'h', 'i']
        assert all(isinstance(cell, Cell) for row in grid for cell in row)
    
    def test_add_line_to_grid_multiple_lines_with_newlines(self):
        """Test adding multiple lines with newline characters."""
        grid = []
        add_line_to_grid(grid, "123\n")
        add_line_to_grid(grid, "456\n")
        add_line_to_grid(grid, "789")
        
        assert len(grid) == 3
        assert [cell.character for cell in grid[0]] == ['1', '2', '3']
        assert [cell.character for cell in grid[1]] == ['4', '5', '6']
        assert [cell.character for cell in grid[2]] == ['7', '8', '9']
        assert all(isinstance(cell, Cell) for row in grid for cell in row)
    
    def test_add_line_to_grid_empty_line(self):
        """Test adding an empty line (after stripping)."""
        grid = []
        add_line_to_grid(grid, "\n")
        
        assert len(grid) == 1
        assert grid[0] == []
    
    def test_add_line_to_grid_special_characters(self):
        """Test adding a line with special characters."""
        grid = []
        add_line_to_grid(grid, "a.b-c_d")
        
        assert len(grid) == 1
        assert len(grid[0]) == 7
        assert [cell.character for cell in grid[0]] == ['a', '.', 'b', '-', 'c', '_', 'd']
        assert all(isinstance(cell, Cell) for cell in grid[0])
        # Verify special character types
        assert grid[0][1].type == CellType.EMPTY  # '.' should be EMPTY

class TestGrid:
    def test_grid_init(self):
        """Test that Grid initializes correctly with grid data."""
        grid_data = [[], [Cell('.'), Cell('.')]]
        grid_obj = Grid(grid_data)
        assert grid_obj.grid == grid_data
        assert grid_obj.split_count == 0

class TestBuildGrid:
    def test_build_grid_small_input(self):
        """Test building grid from day7input_small.txt file."""
        with open("inputs/day7input_small.txt", "r") as file:
            grid_obj = build_grid(file)
        
        grid = grid_obj.grid
        # The grid starts with one empty row, then has 16 rows from the file
        assert len(grid) == 17  # 1 empty row + 16 file rows
        
        # First row should be empty (initial state)
        assert grid[0] == []
        
        # Verify first line from file (row 1)
        assert len(grid[1]) == 15
        assert [cell.character for cell in grid[1]] == ['.', '.', '.', '.', '.', '.', '.', 'S', '.', '.', '.', '.', '.', '.', '.']
        assert grid[1][7].type == CellType.STARTER  # 'S' should be STARTER
        assert all(cell.type == CellType.EMPTY for i, cell in enumerate(grid[1]) if i != 7)
        
        # Verify second line from file (row 2)
        assert len(grid[2]) == 15
        assert [cell.character for cell in grid[2]] == ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']
        assert all(cell.type == CellType.EMPTY for cell in grid[2])
        
        # Verify third line from file (row 3)
        assert len(grid[3]) == 15
        assert [cell.character for cell in grid[3]] == ['.', '.', '.', '.', '.', '.', '.', '^', '.', '.', '.', '.', '.', '.', '.']
        assert grid[3][7].type == CellType.SPLITTER  # '^' should be SPLITTER
        assert all(cell.type == CellType.EMPTY for i, cell in enumerate(grid[3]) if i != 7)
        
        # Verify a line with multiple characters (row 5)
        assert len(grid[5]) == 15
        assert [cell.character for cell in grid[5]] == ['.', '.', '.', '.', '.', '.', '^', '.', '^', '.', '.', '.', '.', '.', '.']
        assert grid[5][6].type == CellType.SPLITTER
        assert grid[5][8].type == CellType.SPLITTER
        
        # Verify second to last line from file (row 15)
        assert len(grid[15]) == 15
        assert [cell.character for cell in grid[15]] == ['.', '^', '.', '^', '.', '^', '.', '^', '.', '^', '.', '.', '.', '^', '.']
        assert all(cell.type == CellType.SPLITTER for i, cell in enumerate(grid[15]) if grid[15][i].character == '^')
        
        # Verify last line from file (row 16) - all dots
        assert len(grid[16]) == 15
        assert [cell.character for cell in grid[16]] == ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']
        assert all(cell.type == CellType.EMPTY for cell in grid[16])
        
        # Verify all cells are Cell objects
        assert all(isinstance(cell, Cell) for row in grid[1:] for cell in row)
        
        # Verify it's a Grid object with split_count
        assert isinstance(grid_obj, Grid)
        assert grid_obj.split_count == 0
    
    def test_build_grid_structure(self):
        """Test that build_grid creates correct grid structure."""
        import io
        file_content = "abc\ndef\nghi"
        file = io.StringIO(file_content)
        grid_obj = build_grid(file)
        grid = grid_obj.grid
        
        # Should have 1 empty row + 3 file rows = 4 rows total
        assert len(grid) == 4
        assert grid[0] == []  # Initial empty row
        assert [cell.character for cell in grid[1]] == ['a', 'b', 'c']
        assert [cell.character for cell in grid[2]] == ['d', 'e', 'f']
        assert [cell.character for cell in grid[3]] == ['g', 'h', 'i']
        assert all(isinstance(cell, Cell) for row in grid[1:] for cell in row)
        assert isinstance(grid_obj, Grid)
    
    def test_build_grid_empty_file(self):
        """Test building grid from an empty file."""
        import io
        file = io.StringIO("")
        grid_obj = build_grid(file)
        grid = grid_obj.grid
        
        # Should only have the initial empty row
        assert len(grid) == 1
        assert grid[0] == []
        assert isinstance(grid_obj, Grid)

class TestCellInit:
    def test_cell_init_starter_character(self):
        """Test that Cell correctly identifies 'S' as STARTER type."""
        cell = Cell('S')
        assert cell.character == 'S'
        assert cell.type == CellType.STARTER
    
    def test_cell_init_splitter_character(self):
        """Test that Cell correctly identifies '^' as SPLITTER type."""
        cell = Cell('^')
        assert cell.character == '^'
        assert cell.type == CellType.SPLITTER
    
    def test_cell_init_empty_character_dot(self):
        """Test that Cell correctly identifies '.' as EMPTY type."""
        cell = Cell('.')
        assert cell.character == '.'
        assert cell.type == CellType.EMPTY
    
    def test_cell_init_empty_character_other(self):
        """Test that Cell correctly identifies other characters as EMPTY type."""
        cell = Cell('a')
        assert cell.character == 'a'
        assert cell.type == CellType.EMPTY
        
        cell2 = Cell('X')
        assert cell2.character == 'X'
        assert cell2.type == CellType.EMPTY
        
        cell3 = Cell(' ')
        assert cell3.character == ' '
        assert cell3.type == CellType.EMPTY
    
    def test_cell_init_preserves_character(self):
        """Test that Cell preserves the original character regardless of type."""
        test_chars = ['S', '^', '.', 'a', '1', '@', '#']
        for char in test_chars:
            cell = Cell(char)
            assert cell.character == char

class TestBeamInit:
    def test_beam_init_sets_position(self):
        """Test that Beam correctly sets row and column position."""
        beam = Beam(5, 10)
        assert beam.row == 5
        assert beam.col == 10
    
    def test_beam_init_is_ended_starts_false(self):
        """Test that Beam's is_ended property starts as False."""
        beam = Beam(0, 0)
        assert beam.is_ended == False

class TestBeamStepDown:
    def test_beam_step_down_moves_one_row(self):
        """Test that beam moves down one row when possible."""
        grid_data = [[], [Cell('.'), Cell('.')], [Cell('.'), Cell('.')]]
        grid_obj = Grid(grid_data)
        beam = Beam(1, 0)
        beams = [beam]
        beam.step_down(grid_obj, beams)
        assert beam.row == 2
        assert beam.col == 0
        assert beam.is_ended == False
    
    def test_beam_step_down_ends_at_bottom(self):
        """Test that beam ends when hitting bottom of grid."""
        grid_data = [[], [Cell('.'), Cell('.')]]
        grid_obj = Grid(grid_data)
        beam = Beam(1, 0)
        beams = [beam]
        beam.step_down(grid_obj, beams)
        assert beam.row == 1  # Should not move
        assert beam.is_ended == True
    
    def test_beam_step_down_ends_at_splitter(self):
        """Test that beam ends when hitting SPLITTER cell and increments split_count."""
        grid_data = [[], [Cell('.'), Cell('.')], [Cell('.'), Cell('^')]]
        grid_obj = Grid(grid_data)
        beam = Beam(1, 1)
        beams = [beam]
        assert grid_obj.split_count == 0
        beam.step_down(grid_obj, beams)
        assert beam.row == 2  # Should move to splitter cell, then end
        assert beam.is_ended == True
        assert grid_obj.split_count == 1
    
    def test_beam_step_down_continues_through_empty(self):
        """Test that beam continues through EMPTY cells."""
        grid_data = [[], [Cell('.'), Cell('.')], [Cell('.'), Cell('.')], [Cell('.'), Cell('.')]]
        grid_obj = Grid(grid_data)
        beam = Beam(1, 0)
        beams = [beam]
        beam.step_down(grid_obj, beams)
        assert beam.row == 2
        assert beam.is_ended == False
        beam.step_down(grid_obj, beams)
        assert beam.row == 3
        assert beam.is_ended == False
    
    def test_beam_step_down_does_nothing_when_ended(self):
        """Test that step_down does nothing if beam is already ended."""
        grid_data = [[], [Cell('.'), Cell('.')], [Cell('.'), Cell('.')]]
        grid_obj = Grid(grid_data)
        beam = Beam(1, 0)
        beam.is_ended = True
        initial_row = beam.row
        initial_count = grid_obj.split_count
        beams = [beam]
        beam.step_down(grid_obj, beams)
        assert beam.row == initial_row
        assert beam.is_ended == True
        assert grid_obj.split_count == initial_count  # Should not increment if already ended

class TestSplitterBeamCreation:
    def test_beam_creates_left_right_beams_at_splitter(self):
        """Test that beam creates left and right beams when hitting a SPLITTER."""
        grid_data = [[], [Cell('.'), Cell('.')], [Cell('.'), Cell('^'), Cell('.')], [Cell('.'), Cell('.'), Cell('.')]]
        grid_obj = Grid(grid_data)
        beam = Beam(1, 1)
        beams = [beam]
        # Step the beam until it hits the splitter
        beam.step_down(grid_obj, beams)
        # Should have created left and right beams
        assert len(beams) == 3
        assert beam.is_ended == True
        # Check left beam exists at (2, 0)
        left_beam = next((b for b in beams if b.row == 2 and b.col == 0), None)
        assert left_beam is not None
        assert left_beam.is_ended == False
        # Check right beam exists at (2, 2)
        right_beam = next((b for b in beams if b.row == 2 and b.col == 2), None)
        assert right_beam is not None
        assert right_beam.is_ended == False
        # Split count should be 1
        assert grid_obj.split_count == 1
    
    def test_beam_splitter_prevents_duplicate_beams(self):
        """Test that splitter beam creation prevents duplicates."""
        grid_data = [[], [Cell('.'), Cell('.')], [Cell('.'), Cell('^'), Cell('.')], [Cell('.'), Cell('.'), Cell('.')]]
        grid_obj = Grid(grid_data)
        # Create existing beam at left position
        beams = [Beam(1, 1), Beam(2, 0)]
        # Step the first beam until it hits the splitter
        beams[0].step_down(grid_obj, beams)
        # Should only create right beam, not duplicate left beam
        assert len(beams) == 3  # Original 2 + 1 new right beam
        # Check that left beam position (2, 0) only has one beam
        left_beams = [b for b in beams if b.row == 2 and b.col == 0]
        assert len(left_beams) == 1
        # Check right beam was created
        right_beam = next((b for b in beams if b.row == 2 and b.col == 2), None)
        assert right_beam is not None
    
    def test_beam_splitter_at_left_edge(self):
        """Test that splitter at left edge only creates right beam."""
        grid_data = [[], [Cell('.'), Cell('.')], [Cell('^'), Cell('.')], [Cell('.'), Cell('.')]]
        grid_obj = Grid(grid_data)
        beam = Beam(1, 0)
        beams = [beam]
        beam.step_down(grid_obj, beams)
        # Should only create right beam (no left beam possible)
        assert len(beams) == 2  # Original + right beam
        # Check right beam exists at (2, 1)
        right_beam = next((b for b in beams if b.row == 2 and b.col == 1), None)
        assert right_beam is not None
        assert grid_obj.split_count == 1
    
    def test_beam_splitter_at_right_edge(self):
        """Test that splitter at right edge only creates left beam."""
        grid_data = [[], [Cell('.'), Cell('.')], [Cell('.'), Cell('^')], [Cell('.'), Cell('.')]]
        grid_obj = Grid(grid_data)
        beam = Beam(1, 1)
        beams = [beam]
        beam.step_down(grid_obj, beams)
        # Should only create left beam (no right beam possible)
        assert len(beams) == 2  # Original + left beam
        # Check left beam exists at (2, 0)
        left_beam = next((b for b in beams if b.row == 2 and b.col == 0), None)
        assert left_beam is not None
        assert grid_obj.split_count == 1
    
    def test_beam_splitter_does_not_process_new_beams(self):
        """Test that newly created beams from splitters are not automatically processed."""
        grid_data = [[], [Cell('.'), Cell('.')], [Cell('.'), Cell('^'), Cell('.')], [Cell('.'), Cell('.'), Cell('.')]]
        grid_obj = Grid(grid_data)
        beam = Beam(1, 1)
        beams = [beam]
        # Step the beam until it hits the splitter
        beam.step_down(grid_obj, beams)
        # New beams should be created but not processed (not ended)
        assert len(beams) == 3
        left_beam = next((b for b in beams if b.row == 2 and b.col == 0), None)
        right_beam = next((b for b in beams if b.row == 2 and b.col == 2), None)
        assert left_beam is not None
        assert right_beam is not None
        # New beams should not be ended (they haven't been processed yet)
        assert left_beam.is_ended == False
        assert right_beam.is_ended == False

class TestGenerateBeamsFromStarters:
    def test_generate_beams_finds_single_starter(self):
        """Test that generate_beams finds a single STARTER cell."""
        grid = [[], [Cell('.'), Cell('S'), Cell('.')], [Cell('.'), Cell('.'), Cell('.')]]
        beams = generate_beams_from_starters(grid)
        assert len(beams) == 1
        assert beams[0].row == 2
        assert beams[0].col == 1
        assert beams[0].is_ended == False
    
    def test_generate_beams_finds_multiple_starters(self):
        """Test that generate_beams finds multiple STARTER cells."""
        grid = [[], [Cell('S'), Cell('.'), Cell('S')], [Cell('.'), Cell('.'), Cell('.')]]
        beams = generate_beams_from_starters(grid)
        assert len(beams) == 2
        assert beams[0].row == 2
        assert beams[0].col == 0
        assert beams[1].row == 2
        assert beams[1].col == 2
    
    def test_generate_beams_handles_starter_at_bottom(self):
        """Test that generate_beams doesn't create beam if STARTER is at bottom."""
        grid = [[], [Cell('.'), Cell('S'), Cell('.')]]
        beams = generate_beams_from_starters(grid)
        assert len(beams) == 0
    
    def test_generate_beams_handles_no_starters(self):
        """Test that generate_beams returns empty list when no STARTER cells exist."""
        grid = [[], [Cell('.'), Cell('.'), Cell('.')], [Cell('.'), Cell('.'), Cell('.')]]
        beams = generate_beams_from_starters(grid)
        assert len(beams) == 0
    
    def test_generate_beams_with_small_input(self):
        """Test generate_beams with the small input file structure."""
        with open("inputs/day7input_small.txt", "r") as file:
            grid_obj = build_grid(file)
        beams = generate_beams_from_starters(grid_obj.grid)
        # Should find the 'S' in row 1, column 7 (0-indexed)
        assert len(beams) == 1
        assert beams[0].row == 2  # Row below the STARTER
        assert beams[0].col == 7  # Same column as STARTER
    
    def test_generate_beams_prevents_duplicate_at_position(self):
        """Test that generate_beams doesn't create beam if one already exists at that position."""
        grid = [[], [Cell('.'), Cell('S'), Cell('.')], [Cell('.'), Cell('.'), Cell('.')]]
        # Create an existing beam at the position where a new beam would be created
        existing_beams = [Beam(2, 1)]
        beams = generate_beams_from_starters(grid, existing_beams)
        # Should not create a duplicate beam
        assert len(beams) == 0
    
    def test_generate_beams_creates_beam_when_no_duplicate(self):
        """Test that generate_beams creates beam when no beam exists at that position."""
        grid = [[], [Cell('.'), Cell('S'), Cell('.')], [Cell('.'), Cell('.'), Cell('.')]]
        # Create an existing beam at a different position
        existing_beams = [Beam(2, 0)]
        beams = generate_beams_from_starters(grid, existing_beams)
        # Should create a beam at the STARTER's position (2, 1)
        assert len(beams) == 1
        assert beams[0].row == 2
        assert beams[0].col == 1
    
    def test_generate_beams_handles_multiple_starters_with_duplicates(self):
        """Test that generate_beams handles multiple STARTERs, preventing duplicates."""
        grid = [[], [Cell('S'), Cell('S'), Cell('S')], [Cell('.'), Cell('.'), Cell('.')]]
        # Create existing beams at positions (2, 0) and (2, 2)
        existing_beams = [Beam(2, 0), Beam(2, 2)]
        beams = generate_beams_from_starters(grid, existing_beams)
        # Should only create one beam at (2, 1), skipping duplicates at (2, 0) and (2, 2)
        assert len(beams) == 1
        assert beams[0].row == 2
        assert beams[0].col == 1
    
    def test_generate_beams_handles_all_duplicates(self):
        """Test that generate_beams returns empty list when all positions are duplicates."""
        grid = [[], [Cell('S'), Cell('S')], [Cell('.'), Cell('.')]]
        # Create existing beams at all positions where new beams would be created
        existing_beams = [Beam(2, 0), Beam(2, 1)]
        beams = generate_beams_from_starters(grid, existing_beams)
        # Should not create any duplicate beams
        assert len(beams) == 0
    
    def test_generate_beams_with_empty_existing_beams(self):
        """Test that generate_beams works correctly with empty existing_beams list."""
        grid = [[], [Cell('.'), Cell('S'), Cell('.')], [Cell('.'), Cell('.'), Cell('.')]]
        existing_beams = []
        beams = generate_beams_from_starters(grid, existing_beams)
        # Should create beam normally
        assert len(beams) == 1
        assert beams[0].row == 2
        assert beams[0].col == 1

class TestProcessBeams:
    def test_process_beams_steps_until_end(self):
        """Test that process_beams steps all beams until they end."""
        grid_data = [[], [Cell('.'), Cell('.')], [Cell('.'), Cell('.')], [Cell('.'), Cell('.')]]
        grid_obj = Grid(grid_data)
        beams = [Beam(1, 0), Beam(1, 1)]
        process_beams(beams, grid_obj)
        # Both beams should end at bottom (row 3)
        assert all(beam.is_ended for beam in beams)
        assert beams[0].row == 3
        assert beams[1].row == 3
    
    def test_process_beams_stops_at_splitter(self):
        """Test that process_beams stops beams at SPLITTER cells and increments split_count."""
        grid_data = [[], [Cell('.'), Cell('.')], [Cell('.'), Cell('^')], [Cell('.'), Cell('.')]]
        grid_obj = Grid(grid_data)
        beams = [Beam(1, 1)]
        assert grid_obj.split_count == 0
        process_beams(beams, grid_obj)
        # Beam should end at row 2 (the splitter), not continue to row 3
        assert beams[0].is_ended == True
        assert beams[0].row == 2
        assert grid_obj.split_count == 1
    
    def test_process_beams_handles_multiple_beams(self):
        """Test that process_beams handles multiple beams correctly."""
        grid_data = [[], [Cell('.'), Cell('.'), Cell('.')], [Cell('.'), Cell('^'), Cell('.')], [Cell('.'), Cell('.'), Cell('.')]]
        grid_obj = Grid(grid_data)
        beams = [Beam(1, 0), Beam(1, 1), Beam(1, 2)]
        process_beams(beams, grid_obj)
        # All beams should be ended
        assert all(beam.is_ended for beam in beams)
        # Beam at col 1 should stop at row 2 (splitter)
        assert beams[1].row == 2
        # Other beams should continue to row 3
        assert beams[0].row == 3
        assert beams[2].row == 3
        # Split count should be 1 (one beam hit a splitter)
        assert grid_obj.split_count == 1
    
    def test_process_beams_with_empty_list(self):
        """Test that process_beams handles empty beam list."""
        grid_data = [[], [Cell('.'), Cell('.')]]
        grid_obj = Grid(grid_data)
        beams = []
        result = process_beams(beams, grid_obj)
        assert result == []
        assert len(result) == 0
    
    def test_process_beams_multiple_splitters_increment_count(self):
        """Test that multiple beams hitting splitters increment split_count correctly."""
        grid_data = [[], [Cell('.'), Cell('.'), Cell('.')], [Cell('.'), Cell('^'), Cell('^')], [Cell('.'), Cell('.'), Cell('.')]]
        grid_obj = Grid(grid_data)
        beams = [Beam(1, 1), Beam(1, 2)]
        process_beams(beams, grid_obj)
        # Both beams should hit splitters
        assert grid_obj.split_count == 2

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
