from bitarray import bitarray
import json

def read_compressed_file(filename):
    # Reads the compressed binary file
    with open(filename, "rb") as file:
        padding_length = int.from_bytes(file.read(1), byteorder='big')  # First byte is padding length
        compressed_data = bitarray()
        compressed_data.fromfile(file)
        if padding_length > 0:
            compressed_data = compressed_data[:-padding_length]  # Remove the padding
    return compressed_data


def read_huffman_codes(filename):
    # Reads the Huffman codes from a JSON file
    with open(filename, "r") as file:
        codes = json.load(file)
    # Reverse the mapping for decoding
    return {value: key for key, value in codes.items()}


def decode_text(codes, compressed_data):
    # Handle single character case (only one code)
    if len(codes) == 1:
        single_char = next(iter(codes.values()))
        return single_char * len(compressed_data)

    # Decode the binary data for normal cases
    current_code = ""
    decoded_text = []

    for bit in compressed_data:
        current_code += "1" if bit else "0"
        if current_code in codes:  # If a valid code is found
            decoded_text.append(codes[current_code])
            current_code = ""  # Reset for the next character
    return "".join(decoded_text)


if __name__ == "__main__":
    # Step 1: Read the compressed binary data
    compressed_data = read_compressed_file("compressed.bin")

    # Step 2: Read the Huffman codes from the JSON file
    huffman_codes = read_huffman_codes("Codes.json")

    # Step 3: Decode the compressed binary data
    decompressed_text = decode_text(huffman_codes, compressed_data)

    # Step 4: Write the decompressed text to a file
    with open("decompressed.txt", "w") as file:
        file.write(decompressed_text)

    print("Decompression complete! The original text has been restored.")
