# Day 3: Advent of Code 2025.
# Part 1: Find the largest two-digit number anywhere in a given row, 
# without reordering the digits. Digits do not need to be adjacent.
# Part 2: Find the largest 12-digit number that can be formed from the line,
# where each digit must come from a later position than the previous digit.

def main():
    part_one_sum = 0
    part_two_sum = 0
    with open("inputs/day3input.txt", "r") as file:
        for line in file:
            # Because Advent has a second part, we'll do processing for each
            # part in a separate function.
            part_one_sum += part_one(line)
            part_two_sum += find_battery_output(line, 12)
    print(f"Part 1: The sum of the largest two-digit numbers is: {part_one_sum}")
    print(f"Part 2: The sum of the largest 12-digit numbers is: {part_two_sum}")

def part_one(line):
    # Find the largest two-digit number using find_battery_output
    return find_battery_output(line, 2)

def find_battery_output(line, num_digits):
    # Find the largest N-digit number that can be formed from the line,
    # where each digit must come from a later position than the previous digit.
    
    # strip the line, so that we don't have to deal with whitespace
    line = line.strip()
    
    # If the line doesn't have enough digits, return 0
    if len(line) < num_digits:
        return 0
    
    # Store the indices of the selected digits
    digit_indices = []
    
    # For each digit position, find the largest available digit
    # The first digit can be from position 0 to len(line) - num_digits
    # The second digit can be from position (first_index + 1) to len(line) - (num_digits - 1)
    # And so on...
    
    start_index = 0
    for digit_pos in range(num_digits):
        # Calculate the maximum index we can search for this digit
        # We need to leave enough digits for the remaining positions
        max_index = len(line) - (num_digits - digit_pos)
        
        # Find the largest digit in the available range
        current_largest_index = start_index
        for i in range(start_index, max_index + 1):
            if int(line[i]) > int(line[current_largest_index]):
                current_largest_index = i
        
        digit_indices.append(current_largest_index)
        start_index = current_largest_index + 1
    
    # Build the N-digit number
    result = 0
    for i, index in enumerate(digit_indices):
        result = result * 10 + int(line[index])
    
    return result

if __name__ == "__main__":
    main()