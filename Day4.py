def main():
    with open("inputs/day4input.txt", "r") as file:
        grid = build_grid(file)
        count = remove_objects_iteratively(grid, 3)
    print(f"The number of objects removed is: {count}")

# Build a grid from the input file
def build_grid(file):
    grid = []
    # For each line in the file, append the line to the grid
    for line in file:
        row = []
        for char in line.strip():
            row.append(char)
        grid.append(row)
    return(grid)

# Count the surrounding objects for a given position in the grid
# Skipping the position itself and checking if the position is within the grid
# x is the column index, y is the row index
def count_surrounding_objects(grid, x, y):
    count = 0
    # Check the 8 surrounding positions, skipping the position itself
    # x is column, y is row, so we access grid[row][column] = grid[y][x]
    for row in range(y-1, y+2):
        for col in range(x-1, x+2):
            if row == y and col == x:
                continue
            if row >= 0 and row < len(grid) and col >= 0 and col < len(grid[0]):
                if grid[row][col] == '@':
                    count += 1
    return count

# Return the count of cells with less than or equal the limit
# in count of surrounding objects  
def get_total_count_below_limit(grid, limit):
    count = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            # Ensure there is an object at the position
            if grid[y][x] != '@':
                continue
            if count_surrounding_objects(grid, x, y) <= limit:
                count += 1
    return count

# Iteratively remove objects that have <= limit surrounding objects
# Mark removed objects as 'X' and repeat until no more can be removed
# Returns the total count of removed objects
def remove_objects_iteratively(grid, limit):
    total_removed = 0
    
    while True:
        # Find all objects that can be removed in this iteration
        to_remove = []
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                # Only consider '@' objects (not already removed 'X')
                if grid[y][x] != '@':
                    continue
                # Check if this object has <= limit surrounding objects
                if count_surrounding_objects(grid, x, y) <= limit:
                    to_remove.append((x, y))
        
        # If no objects to remove, we're done
        if len(to_remove) == 0:
            break
        
        # Remove all objects found in this iteration
        for x, y in to_remove:
            grid[y][x] = 'X'
            total_removed += 1
        
        # After removing objects, surrounding counts change for neighbors
        # So we'll recalculate in the next iteration
    
    return total_removed

if __name__ == "__main__":
    main()