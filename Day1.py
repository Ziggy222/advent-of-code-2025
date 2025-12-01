def main():
    curr_num = 50
    part1_num_zeros = 0
    part2_num_zeros = 0
    
    with open("inputs/day1input.txt", "r") as file:
        for line in file:
            # Process the change in the dial
            # Get the direction from the first character
            direction = line[0].upper()
            # Get the amount from the rest of the line
            amount = int(line[1:].strip())
            # Process the change in the dial
            if direction == "R":
                # If R, we want to rotate right by the amount, wrapping at 99 and 0
                # We can use modulo arithmetic to wrap around
                curr_num, passed_zeros = rotate_right(curr_num, amount)
                part2_num_zeros += passed_zeros
            elif direction == "L":
                # If L, we want to rotate left by the amount, wrapping at 99 and 0
                # We can use modulo arithmetic to wrap around
                curr_num, passed_zeros = rotate_left(curr_num, amount)
                part2_num_zeros += passed_zeros
            else:
                raise ValueError(f"Invalid direction: {direction}")
            # If the number is 0, we have a zero
            if curr_num == 0:
                part1_num_zeros += 1
    print(f"Part 1: The number of zeros is: {part1_num_zeros}")
    print(f"Part 2: The number of zeros is: {part2_num_zeros}")

def rotate_left(num, amount):
    passed_zeros = 0
    for i in range(amount):
        num = (num - 1) % 100
        if num == 0:
            passed_zeros += 1
    return num, passed_zeros

def rotate_right(num, amount):
    passed_zeros = 0
    for i in range(amount):
        num = (num + 1) % 100
        if num == 0:
            passed_zeros += 1
    return num, passed_zeros

if __name__ == "__main__":
    main()