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

# Step 1: Read and get frequancy of data
original_data = read_file("input.txt")
frequency = getFrequency(original_data)
print(frequency)
# Step 2: Compress the data

