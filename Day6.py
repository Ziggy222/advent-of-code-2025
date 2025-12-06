def read_file_columns(file):
    """Read a file and parse numbers from columns and operations from the last row.
    
    Args:
        file: An open file object
    
    Returns:
        A tuple of (columns, operations) where:
        - columns: list of lists, each inner list contains numbers from one column
        - operations: list of operation characters ('+' or '*') for each column
    """
    lines = file.readlines()
    
    # Separate data rows from operation row (last row)
    data_lines = lines[:-1]
    operation_line = lines[-1].strip()
    
    # Parse operations from the last line
    operations = []
    for char in operation_line.split():
        if char in ['+', '*']:
            operations.append(char)
    
    # Determine number of columns from the operation line
    num_columns = len(operations)
    
    # Initialize columns as empty lists
    columns = [[] for _ in range(num_columns)]
    
    # Parse numbers from each data line
    for line in data_lines:
        # Split by whitespace and filter out empty strings
        parts = line.split()
        # Convert to integers and add to respective columns
        for i, part in enumerate(parts):
            if i < num_columns:
                try:
                    columns[i].append(int(part))
                except ValueError:
                    # Skip if not a valid number
                    pass
    
    return columns, operations

def build_stacked_numbers(column_strings):
    """Build numbers by reading digits vertically from top to bottom, right-to-left.
    
    Takes a list of number strings. For each position from right to left (0=rightmost),
    reads the digit at that position from each number (if it exists), reading from
    top to bottom to form a number.
    
    Args:
        column_strings: List of strings representing numbers (e.g., ["64", "23", "314"])
    
    Returns:
        List of numbers built by reading digits vertically
    """
    if not column_strings:
        return []
    
    # Convert to strings
    num_strings = [str(num) for num in column_strings]
    max_len = max(len(s) for s in num_strings)
    
    stacked_numbers = []
    
    # Read from rightmost position (0) to leftmost (max_len-1)
    # Position 0 is the rightmost digit, position 1 is second from right, etc.
    for pos_from_right in range(max_len):
        # For this position from the right, collect digits from each number
        digits = []
        for num_str in num_strings:
            # Calculate position from left: len - 1 - pos_from_right
            pos_from_left = len(num_str) - 1 - pos_from_right
            if pos_from_left >= 0:
                digits.append(num_str[pos_from_left])
        
        # If we have digits, form a number from them (top to bottom)
        if digits:
            number_str = ''.join(digits)
            stacked_numbers.append(int(number_str))
    
    return stacked_numbers

def read_file_columns_stacked(file):
    """Read a file and parse numbers from columns using stacked parsing (right-to-left).
    
    Parses right-to-left in columns. Each number is given its own column, with the
    most significant digit at the top and the least significant digit at the bottom.
    Problems are separated by a column consisting only of spaces. The symbol at
    the bottom is the operator to use.
    
    Args:
        file: An open file object
    
    Returns:
        A tuple of (stacked_columns, operations) where:
        - stacked_columns: list of lists, each inner list contains numbers from one problem column
        - operations: list of operation characters ('+' or '*') for each column
    """
    lines = file.readlines()
    
    # Separate data rows from operation row (last row)
    data_lines = [line.rstrip('\n') for line in lines[:-1]]
    operation_line = lines[-1].rstrip('\n')
    
    # Find the maximum line length
    max_line_len = max(len(line) for line in data_lines + [operation_line])
    
    # Pad all lines to the same length for easier processing
    padded_data = [line.ljust(max_line_len) for line in data_lines]
    padded_ops = operation_line.ljust(max_line_len)
    
    # Process from right to left
    stacked_columns = []
    stacked_operations = []
    current_column_numbers = []
    current_operator = None
    
    # Start from the rightmost character position
    pos = max_line_len - 1
    
    while pos >= 0:
        # Check if this position has any digits in the data rows
        has_digit = any(line[pos].isdigit() for line in padded_data)
        
        if has_digit:
            # Read digits vertically from top to bottom at this position
            digits = []
            for line in padded_data:
                char = line[pos]
                if char.isdigit():
                    digits.append(char)
            
            # Form a number from the digits (read top to bottom)
            if digits:
                number = int(''.join(digits))
                current_column_numbers.append(number)
                
                # Check for operator at this position in the operation line
                if pos < len(padded_ops) and padded_ops[pos] in ['+', '*']:
                    current_operator = padded_ops[pos]
        else:
            # Check if this position is all spaces (column break between problems)
            all_spaces_data = all(line[pos] == ' ' for line in padded_data)
            all_spaces_op = pos >= len(padded_ops) or padded_ops[pos] == ' '
            
            if all_spaces_data and all_spaces_op:
                # This is a separator column - save current problem if we have numbers
                if current_column_numbers:
                    # Numbers are already in correct order (rightmost position = first number)
                    stacked_columns.append(current_column_numbers)
                    stacked_operations.append(current_operator or '+')
                    current_column_numbers = []
                    current_operator = None
            elif pos < len(padded_ops) and padded_ops[pos] in ['+', '*']:
                # Operator without digits - might be at the end of a number column
                if current_operator is None:
                    current_operator = padded_ops[pos]
        
        pos -= 1
    
    # Don't forget the last column if we have numbers
    if current_column_numbers:
        stacked_columns.append(current_column_numbers)
        stacked_operations.append(current_operator or '+')
    
    # Reverse to get left-to-right order (since we processed right-to-left)
    return list(reversed(stacked_columns)), list(reversed(stacked_operations))

def apply_operation(numbers, operation):
    """Apply an operation sequentially to a list of numbers.
    
    Args:
        numbers: A list of numbers
        operation: Either '+' for addition or '*' for multiplication
    
    Returns:
        The result of applying the operation sequentially to all numbers
    """
    if not numbers:
        return 0
    
    if operation == '+':
        result = 0
        for num in numbers:
            result += num
        return result
    elif operation == '*':
        result = 1
        for num in numbers:
            result *= num
        return result
    else:
        raise ValueError(f"Unknown operation: {operation}")

def main():
    # Part 1: Normal parsing
    with open("inputs/day6input.txt", "r") as file:
        columns, operations = read_file_columns(file)
        
        # Apply operation to each column and collect results
        column_results = []
        for i, (column_numbers, operation) in enumerate(zip(columns, operations)):
            result = apply_operation(column_numbers, operation)
            column_results.append(result)
        
        # Sum all column results
        total_sum = sum(column_results)
        print(f"Part 1: The sum of all column results is: {total_sum}")
    
    # Part 2: Stacked parsing (right-to-left)
    with open("inputs/day6input.txt", "r") as file:
        stacked_columns, stacked_operations = read_file_columns_stacked(file)
        
        # Apply operation to each stacked column and collect results
        stacked_results = []
        for column_numbers, operation in zip(stacked_columns, stacked_operations):
            result = apply_operation(column_numbers, operation)
            stacked_results.append(result)
        
        # Sum all stacked column results
        stacked_total = sum(stacked_results)
        print(f"Part 2: The sum of all stacked column results is: {stacked_total}")

if __name__ == "__main__":
    main()