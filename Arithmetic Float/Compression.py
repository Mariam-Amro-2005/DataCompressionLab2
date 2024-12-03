from collections import Counter
import json
import os
import struct

def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print("Error: File not found.")
        return ""
    except PermissionError:
        print("Error: Permission denied.")
        return ""


def calculate_probabilities(file_content):
    if not file_content:
        print("Warning: Input file is empty.")
        return {}

    frequency = dict(Counter(file_content))
    total_chars = sum(frequency.values())
    probabilities = {char: freq / total_chars for char, freq in frequency.items()}
    return dict(sorted(probabilities.items()))  # Sorted by characters


def calculate_ranges(probabilities):
    ranges = {}
    low = 0.0

    for char, prob in probabilities.items():
        high = low + prob
        ranges[char] = (low, high)
        low = high

    return ranges


def save_ranges_to_file(ranges, filename):
    with open(f"{filename}_ranges.json", "w", encoding="utf-8") as file:
        json.dump(ranges, file, indent=4)
    print(f"Ranges saved to {filename}_ranges.json")

def save_compressed_value(filename, num_characters, compressed_value):
    # Save the compressed value to a binary file.
    # Extract the base name without the extension
    base_name, _ = os.path.splitext(filename)
    binary_filename = f"{base_name}_compressed.bin"

    with open(binary_filename, 'wb') as binary_file:
        # Write the number of characters (as an integer)
        binary_file.write(struct.pack('I', num_characters))  # 'I' for unsigned int
        # Write the compressed value (as a float)
        binary_file.write(struct.pack('d', compressed_value))  # 'd' for double
    print(f"Compressed value and character count saved to {binary_filename}")


def arithmetic_compress(input_text, ranges):
    if not input_text or not ranges:
        return 0, None, {}

    low, high = 0.0, 1.0

    for char in input_text:
        if char not in ranges:
            raise ValueError(f"Unexpected character '{char}' in input.")

        char_low, char_high = ranges[char]
        range_width = high - low
        high = low + range_width * char_high
        low = low + range_width * char_low

    compressed_value = (low + high) / 2
    return len(input_text), compressed_value, ranges


def menu():
    print("Arithmetic Compression Tool")
    print("===========================")
    while True:
        print("\nOptions:")
        print("1. Compress a file")
        print("2. Exit")

        choice = input("Enter your choice (1/2): ").strip()

        if choice == "1":
            filename = input("Enter the file name to compress: ").strip()
            if not os.path.exists(filename):
                print(f"Error: File '{filename}' does not exist.")
                continue

            # Read the file content
            input_text = read_file(filename)
            if not input_text:
                print(f"Error: File '{filename}' is empty or unreadable.")
                continue

            # Calculate probabilities and ranges
            probabilities = calculate_probabilities(input_text)
            ranges = calculate_ranges(probabilities)

            # Save ranges to a JSON file
            save_ranges_to_file(ranges, filename)

            # Perform arithmetic compression
            num_characters, compressed_value, original_ranges = arithmetic_compress(input_text, ranges)

            # Save compressed value to binary file
            save_compressed_value(filename, num_characters, compressed_value)

            print("\nCompression Results:")
            print(f"File: {filename}")
            print(f"Number of Characters: {num_characters}")
            print(f"Compressed Value: {compressed_value}")
            print(f"Ranges saved to {filename}_ranges.json")

        elif choice == "2":
            print("Exiting the tool. Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1 or 2.")


# Call the menu to start the program
menu()
