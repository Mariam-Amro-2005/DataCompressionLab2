from collections import Counter
import json
import os
import struct
from decimal import Decimal, getcontext

# Set precision for BigDecimal operations
getcontext().prec = 500

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
    probabilities = {char: Decimal(freq) / Decimal(total_chars) for char, freq in frequency.items()}
    return dict(sorted(probabilities.items()))  # Sorted by characters


def calculate_ranges(probabilities):
    ranges = {}
    low = Decimal(0)

    for char, prob in probabilities.items():
        high = low + prob
        ranges[char] = (low, high)
        low = high

    return ranges


def save_ranges_to_file(ranges, filename):
    base_name, _ = os.path.splitext(filename)
    ranges_str = {char: (str(low), str(high)) for char, (low, high) in ranges.items()}
    with open(f"{base_name}_ranges.json", "w", encoding="utf-8") as file:
        json.dump(ranges_str, file, indent=4)
    print(f"Ranges saved to {base_name}_ranges.json")


def save_compressed_value(filename, num_characters, compressed_value):
    base_name, _ = os.path.splitext(filename)
    binary_filename = f"{base_name}_compressed.bin"

    with open(binary_filename, 'wb') as binary_file:
        binary_file.write(struct.pack('I', num_characters))  # 'I' for unsigned int
        binary_file.write(str(compressed_value).encode('utf-8'))  # Save compressed value as string
    print(f"Compressed value and character count saved to {binary_filename}")


def arithmetic_compress(input_text, ranges):
    if not input_text or not ranges:
        return 0, None, {}

    low, high = Decimal(0), Decimal(1)

    for char in input_text:
        if char not in ranges:
            raise ValueError(f"Unexpected character '{char}' in input.")

        char_low, char_high = ranges[char]
        range_width = high - low
        high = low + range_width * char_high
        low = low + range_width * char_low

    compressed_value = (low + high) / 2
    return len(input_text), compressed_value, ranges


def load_ranges_from_file(filename):
    base_name, _ = os.path.splitext(filename)
    json_filename = f"{base_name}_ranges.json"
    if not os.path.exists(json_filename):
        print(f"Error: Ranges file '{json_filename}' does not exist.")
        return None
    with open(json_filename, "r", encoding="utf-8") as file:
        ranges_str = json.load(file)
        return {char: (Decimal(low), Decimal(high)) for char, (low, high) in ranges_str.items()}


def read_compressed_file(filename):
    base_name, _ = os.path.splitext(filename)
    binary_filename = f"{base_name}_compressed.bin"
    if not os.path.exists(binary_filename):
        print(f"Error: Compressed file '{binary_filename}' does not exist.")
        return None, None
    with open(binary_filename, 'rb') as binary_file:
        num_characters = struct.unpack('I', binary_file.read(4))[0]
        compressed_value = Decimal(binary_file.read().decode('utf-8'))
    return num_characters, compressed_value


def arithmetic_decompress(num_characters, compressed_value, ranges):
    if num_characters is None or compressed_value is None or not ranges:
        print("Error: Missing data for decompression.")
        return ""

    decoded_text = []

    for _ in range(num_characters):
        for char, (low, high) in ranges.items():
            if low <= compressed_value < high:
                decoded_text.append(char)
                range_width = high - low
                compressed_value = (compressed_value - low) / range_width
                break

    return ''.join(decoded_text)


def menu():
    print("Arithmetic Compression Tool")
    print("===========================")
    while True:
        print("\nOptions:")
        print("1. Compress a file")
        print("2. Decompress a file")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == "1":
            filename = "input.txt"
            if not os.path.exists(filename):
                print(f"Error: File '{filename}' does not exist.")
                continue

            input_text = read_file(filename)
            if not input_text:
                print(f"Error: File '{filename}' is empty or unreadable.")
                continue

            probabilities = calculate_probabilities(input_text)
            ranges = calculate_ranges(probabilities)
            save_ranges_to_file(ranges, filename)

            num_characters, compressed_value, original_ranges = arithmetic_compress(input_text, ranges)
            save_compressed_value(filename, num_characters, compressed_value)

            print("\nCompression Results:")
            print(f"File: {filename}")
            print(f"Number of Characters: {num_characters}")
            print(f"Compressed Value: {compressed_value}")
            print(f"Ranges saved to {filename}_ranges.json")
        elif choice == "2":
            filename = "input"
            num_characters, compressed_value = read_compressed_file(filename)
            if num_characters is None or compressed_value is None:
                continue

            ranges = load_ranges_from_file(filename)
            if ranges is None:
                continue

            original_text = arithmetic_decompress(num_characters, compressed_value, ranges)

            base_name, _ = os.path.splitext(filename)
            decompressed_filename = f"{base_name}_decompressed.txt"
            with open(decompressed_filename, "w", encoding="utf-8") as file:
                file.write(original_text)
            print(f"Decompressed text saved to {decompressed_filename}")
        elif choice == "3":
            print("Exiting the tool. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1 or 2.")


# Call the menu to start the program
menu()
