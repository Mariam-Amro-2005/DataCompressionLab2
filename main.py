def read_file(filename):
    """Reads the content of a file and returns it as a string."""
    with open(filename, 'r') as file:
        data = file.read()
    return data


def write_file(filename, data):
    """Writes data to a file."""
    with open(filename, 'w') as file:
        file.write(data)


def read_encoded_from_file(filename):
    """Reads the encoded data (integer codes) from a file and returns them as a list."""
    with open(filename, 'r') as file:
        encoded_data = [int(line.strip()) for line in file]  # Read each line as an integer
    return encoded_data


def write_encoded_to_file(filename, encoded_data):
    """Writes the encoded data to a file, one code per line."""
    with open(filename, 'w') as file:
        for code in encoded_data:
            file.write(f"{code}\n")  # Write each code on a new line


def initialize_dictionary():
    dictionary = {}
    for i in range(256):
        dictionary[i] = chr(i)
    return dictionary


def add_new_entry(key, value, dictionary):
    dictionary[key] = value


def encode(data):
    # Initialize dictionary with single characters
    reverse_dictionary = {chr(i): i for i in range(256)}
    tags = []
    current_code = 256  # Start new codes from 256 (ASCII range ends at 255)

    # Looping through data and encoding
    i = 0
    while i < len(data):
        # Finding the longest match
        length = 1
        while i + length <= len(data) and data[i:i + length] in reverse_dictionary:
            length += 1

        # Get the longest matched string in the dictionary
        match = data[i:i + length - 1]
        tags.append(reverse_dictionary[match])  # Store the code for this match

        # Add new sequence (match + next character) to both dictionaries
        if i + length <= len(data):  # Ensure there's a next character to add
            next_seq = data[i:i + length]
            reverse_dictionary[next_seq] = current_code
            current_code += 1

        # Move index forward by the length of the matched sequence
        i += length - 1

    return tags


fileName = read_file("input.txt")
encoded = encode(fileName)

print(encoded)
