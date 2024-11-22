import heapq
from collections import defaultdict, Counter

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # Define comparison operators for priority queue
    def __lt__(self, other):
        return self.freq < other.freq

def getFrequency(data):
    # Returns the frequency of each character in the input string.
    frequency = {}
    for char in data:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1
    # reverse the dictionary to sort by frequency in accending order
    frequency = dict(sorted(frequency.items(), key=lambda item: item[1]))


    #frequency = dict(sorted(frequency.items(), key=lambda item: item[1], reverse=True))

    return frequency

def read_file(filename):
    # Reads the content of a file and returns it as a string.
    with open(filename, 'r') as file:
        data = file.read()
    return data

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

# Generate Huffman Codes
def generate_codes(root, current_code="", codes=None):
    if codes is None:
        codes = {}
    if root is not None:
        if root.char is not None:  # Leaf node
            codes[root.char] = current_code
        generate_codes(root.left, current_code + "0", codes)
        generate_codes(root.right, current_code + "1", codes)
    return codes

# Compress the text
def huffman_compress(text):

    frequency = getFrequency(original_data)

    # Build Huffman Tree
    root = build_huffman_tree(frequency)

    # Generate codes
    codes = generate_codes(root)
    with open("Codes.txt", "w") as file:
        for char, freq in codes.items():
            file.write(char + " " + str(freq) + "\n")
    print("Generated Huffman Codes:", codes)

    # Encode the text
    encoded_text = "".join(codes[char] for char in text)
    return encoded_text, root

# Decompress the encoded text


# Example Usage
if __name__ == "__main__":
    original_data = read_file("input.txt")

    # Compression
    encoded_text, huffman_tree = huffman_compress(original_data)
    print("Encoded Text:", encoded_text)

    with open("output.txt", "w") as file:
        file.write(encoded_text)


