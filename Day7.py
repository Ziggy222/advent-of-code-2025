from enum import Enum

# Characters which will need special processing
# All other characters will be treated as empty cells
special_characters = ['S', '^']

class CellType(Enum):
    STARTER = 'S'
    SPLITTER = '^'
    EMPTY = '.'

class Cell:
    def __init__(self, character):
        self.character = character
        if character == 'S':
            self.type = CellType.STARTER
        elif character == '^':
            self.type = CellType.SPLITTER
        else:
            self.type = CellType.EMPTY

class Grid:
    def __init__(self, grid_data):
        self.grid = grid_data
        self.split_count = 0
        self.counted_splitters = set()  # Track which splitter positions have been counted

class Beam:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_ended = False
    
    def step_down(self, grid_obj, all_beams):
        """Move beam one step down, checking for end conditions.
        
        Args:
            grid_obj: Grid instance containing the grid and split_count
            all_beams: List of all beams (may be modified to add new beams)
        """
        if self.is_ended:
            return
        
        grid = grid_obj.grid
        
        # Check if next row is out of bounds (bottom of grid)
        if self.row + 1 >= len(grid):
            self.is_ended = True
            return
        
        # Move to next row (same column)
        self.row = self.row + 1
        
        # Check if current cell is a SPLITTER (after moving)
        if self.row < len(grid) and self.col < len(grid[self.row]):
            current_cell = grid[self.row][self.col]
            if current_cell.type == CellType.SPLITTER:
                self.is_ended = True
                # Only increment split count if this splitter hasn't been counted yet
                splitter_pos = (self.row, self.col)
                if splitter_pos not in grid_obj.counted_splitters:
                    grid_obj.split_count += 1
                    grid_obj.counted_splitters.add(splitter_pos)
                
                
                # Create left and right beams
                splitter_row = self.row
                splitter_col = self.col
                
                # Create set of existing beam positions for duplicate checking
                existing_positions = {(beam.row, beam.col) for beam in all_beams}
                
                # Create left beam (col - 1) if cell exists
                if splitter_col - 1 >= 0 and splitter_col - 1 < len(grid[splitter_row]):
                    left_pos = (splitter_row, splitter_col - 1)
                    if left_pos not in existing_positions:
                        left_beam = Beam(splitter_row, splitter_col - 1)
                        # If the left position is also a splitter, the beam should end immediately
                        # (but we don't count it as a split since it was created there, not moved into)
                        if grid[splitter_row][splitter_col - 1].type == CellType.SPLITTER:
                            left_beam.is_ended = True
                        all_beams.append(left_beam)
                
                # Create right beam (col + 1) if cell exists
                if splitter_col + 1 < len(grid[splitter_row]):
                    right_pos = (splitter_row, splitter_col + 1)
                    if right_pos not in existing_positions:
                        right_beam = Beam(splitter_row, splitter_col + 1)
                        # If the right position is also a splitter, the beam should end immediately
                        # (but we don't count it as a split since it was created there, not moved into)
                        if grid[splitter_row][splitter_col + 1].type == CellType.SPLITTER:
                            right_beam.is_ended = True
                        all_beams.append(right_beam)
                
                return

def main():
    with open("inputs/day7input.txt", "r") as file:
        grid_obj = build_grid(file)
        # Generate initial beams from STARTER cells
        beams = generate_beams_from_starters(grid_obj.grid)
        # Process all beams
        process_beams(beams, grid_obj)
        # Print split count
        print(f"Split count: {grid_obj.split_count}")
        
# Builds the grid from the file
def build_grid(file):
    grid = [[]]
    for line in file:
        add_line_to_grid(grid, line)
    return Grid(grid)

# Adds a line to the grid, with no other processing
def add_line_to_grid(grid, line):
    row = []
    for char in line.strip():
        row.append(Cell(char))
    grid.append(row)

# Generate beams from all STARTER cells
def generate_beams_from_starters(grid, existing_beams=None):
    """Find all STARTER cells and create beams in cells directly below them.
    
    Args:
        grid: The grid of cells
        existing_beams: Optional list of existing Beam objects to check for duplicates
    
    Returns:
        List of newly created Beam objects
    """
    if existing_beams is None:
        existing_beams = []
    
    # Create a set of existing beam positions for quick lookup
    existing_positions = {(beam.row, beam.col) for beam in existing_beams}
    
    beams = []
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if cell.type == CellType.STARTER:
                # Check if cell directly below exists
                if row_idx + 1 < len(grid):
                    target_pos = (row_idx + 1, col_idx)
                    # Check if a beam already exists at this position
                    if target_pos not in existing_positions:
                        new_beam = Beam(row_idx + 1, col_idx)
                        # If the target position is a splitter, the beam should end immediately
                        # (but we don't count it as a split since it was created there, not moved into)
                        if grid[row_idx + 1][col_idx].type == CellType.SPLITTER:
                            new_beam.is_ended = True
                        beams.append(new_beam)
    return beams

# Process all beams until they reach an end state
def process_beams(beams, grid_obj):
    """Step all beams downward until they all reach an end state.
    Processes beams continuously, including newly created beams from splitters.
    
    Args:
        beams: List of Beam objects to process
        grid_obj: Grid instance
    """
    # Process all beams continuously using index-based iteration
    # This allows us to process newly created beams as they are added
    index = 0
    while index < len(beams):
        beam = beams[index]
        while not beam.is_ended:
            beam.step_down(grid_obj, beams)
        index += 1
    return beams

if __name__ == "__main__":
    main()
