import re
from collections import deque

def parse_line(line: str) -> tuple[list[bool], list[tuple[int, ...]]]:
    """
    Parse a line to extract target state and buttons.
    
    Args:
        line: Input line in format [.##.] (3) (1,3) (2) {3,5,4,7}
    
    Returns:
        Tuple of (target_state, buttons) where:
        - target_state: list of booleans (False = off, True = on)
        - buttons: list of tuples, each tuple contains indices to toggle
    """
    line = line.strip()
    
    # Extract target state from [ ]
    bracket_match = re.search(r'\[([^\]]+)\]', line)
    if not bracket_match:
        raise ValueError(f"No target state found in brackets: {line}")
    
    target_str = bracket_match.group(1)
    target_state = [char == '#' for char in target_str]
    
    # Extract buttons from ( )
    button_matches = re.findall(r'\(([^)]+)\)', line)
    buttons = []
    for button_str in button_matches:
        # Split by comma and convert to integers
        indices = tuple(int(x.strip()) for x in button_str.split(',') if x.strip())
        if indices:  # Only add non-empty buttons
            buttons.append(indices)
    
    # Curly braces content is ignored
    
    return (target_state, buttons)

def toggle_lights(current_state: list[bool], button: tuple[int, ...]) -> list[bool]:
    """
    Apply a button press to toggle lights at specified indices.
    
    Args:
        current_state: Current state of lights (list of booleans)
        button: Tuple of indices to toggle
    
    Returns:
        New state with toggled lights (doesn't modify input)
    """
    new_state = current_state.copy()
    for index in button:
        if 0 <= index < len(new_state):
            new_state[index] = not new_state[index]
    return new_state

def find_minimum_presses(target_state: list[bool], buttons: list[tuple[int, ...]]) -> int:
    """
    Find the minimum number of button presses needed to reach target state.
    Uses BFS to find shortest path from all-off state to target state.
    
    Args:
        target_state: Desired final state (list of booleans)
        buttons: List of button tuples, each containing indices to toggle
    
    Returns:
        Minimum number of button presses, or -1 if impossible
    """
    num_lights = len(target_state)
    initial_state = tuple([False] * num_lights)
    target_state_tuple = tuple(target_state)
    
    # If already at target, return 0
    if initial_state == target_state_tuple:
        return 0
    
    # BFS setup
    queue = deque([(initial_state, 0)])  # (state, presses_count)
    visited = {initial_state}
    
    while queue:
        current_state, presses = queue.popleft()
        
        # Try each button
        for button in buttons:
            # Convert tuple to list for modification
            current_list = list(current_state)
            new_state_list = toggle_lights(current_list, button)
            new_state = tuple(new_state_list)
            
            # Check if we reached the target
            if new_state == target_state_tuple:
                return presses + 1
            
            # If not visited, add to queue
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, presses + 1))
    
    # Target state unreachable
    return -1

def main():
    """
    Read input file, process each line, and print total minimum button presses.
    """
    total_presses = 0
    
    with open("inputs/day10input.txt", "r") as file:
        for line in file:
            target_state, buttons = parse_line(line)
            min_presses = find_minimum_presses(target_state, buttons)
            if min_presses == -1:
                print(f"Warning: Could not reach target state for line: {line.strip()}")
            else:
                total_presses += min_presses
    
    print(total_presses)

if __name__ == "__main__":
    main()

