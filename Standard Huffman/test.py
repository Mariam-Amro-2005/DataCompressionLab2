import heapq
from collections import Counter
from bitarray import bitarray
import json

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def getFrequency(data):
    return dict(Counter(data))


def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()


def build_huffman_tree(frequency):
    heap = [Node(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]  # Root of the tree


def generate_codes(root, current_code="", codes=None):
    if codes is None:
        codes = {}
    if root.char is not None:  # Single node or leaf
        codes[root.char] = current_code if current_code else "0"  # Default code for single character
    else:
        generate_codes(root.left, current_code + "0", codes)
        generate_codes(root.right, current_code + "1", codes)
    return codes


def write_binary_file(encoded_text, filename):
    bits = bitarray(encoded_text)
    bits.fill()  # Pads with zeros to complete a byte
    padding_length = 8 - (len(encoded_text) % 8) if len(encoded_text) % 8 != 0 else 0
    with open(filename, 'wb') as file:
        # Write the padding length as the first byte
        file.write(bytes([padding_length]))
        bits.tofile(file)


def save_huffman_codes(codes, filename):
    with open(filename, 'w') as file:
        json.dump(codes, file)


def huffman_compress(text):
    frequency = getFrequency(text)

    # Build Huffman Tree
    root = build_huffman_tree(frequency)

    # Generate codes
    codes = generate_codes(root)

    # Save codes to file
    save_huffman_codes(codes, "Codes.json")

    # Encode the text
    encoded_text = "".join(codes[char] for char in text)

    # Write binary data
    write_binary_file(encoded_text, "compressed.bin")

    return root


if __name__ == "__main__":
    original_data = read_file("input.txt")

    # Compression
    huffman_tree = huffman_compress(original_data)
    print("Compression completed!")
