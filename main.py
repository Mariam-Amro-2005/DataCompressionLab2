def lzw_compress(data):
    # Initialize dictionary with single character entries
    reverse_dictionary = {chr(i): i for i in range(256)}
    tags = []
    current_code = 256  # Start new codes from 256 (ASCII range ends at 255)

    # Loop through data and compress
    i = 0
    while i < len(data):
        # Find the longest match in the dictionary
        length = 1
        while i + length <= len(data) and data[i:i + length] in reverse_dictionary:
            length += 1

        # Store code for the longest match found
        match = data[i:i + length - 1]
        tags.append(reverse_dictionary[match])

        # Add new sequence (match + next character) to the dictionary
        if i + length <= len(data):
            next_seq = data[i:i + length]
            reverse_dictionary[next_seq] = current_code
            current_code += 1

        # Move index forward by the length of the matched sequence
        i += length - 1

    return tags


def lzw_decompress(compressed_data):
    # Initialize the dictionary with single character strings
    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}
    
    # First value of compressed data is used to initialize `result`
    preEntry = chr(compressed_data.pop(0))
    result = [preEntry]
    
    # Loop through the compressed data
    for k in compressed_data:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            # Special case when no match pattern in dictionary
            entry = preEntry + preEntry[0]
        else:
            raise ValueError("Bad compressed k: {}".format(k))
        
        result.append(entry)
        
        # Add preEntry + entry[0] to the dictionary
        dictionary[dict_size] = preEntry + entry[0]
        dict_size += 1
        
        # Update preEntry to the current entry
        preEntry = entry
    
    # Join the result list into a single output string
    return ''.join(result)


# File I/O functions
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
        encoded_data = [int(line.strip()) for line in file]
    return encoded_data


def write_encoded_to_file(filename, encoded_data):
    """Writes the encoded data to a file, one code per line."""
    with open(filename, 'w') as file:
        for code in encoded_data:
            file.write(f"{code}\n")



# Step 1: Read and compress data
original_data = read_file("input.txt")
compressed_data = lzw_compress(original_data)
write_encoded_to_file("compressed.txt", compressed_data)

# Step 2: Read compressed data and decompress it
compressed_data_from_file = read_encoded_from_file("compressed.txt")
decompressed_data = lzw_decompress(compressed_data_from_file)
write_file("decompressed.txt", decompressed_data)

print("Compression and decompression complete.")
