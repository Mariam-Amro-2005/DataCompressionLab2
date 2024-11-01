def read_file(filename):
    """Reads the content of a file and returns it as a string."""
    with open(filename, 'r') as file:
        data = file.read()
    return data

def write_file(filename, data):
    """Writes data to a file."""
    with open(filename, 'w') as file:
        file.write(data)