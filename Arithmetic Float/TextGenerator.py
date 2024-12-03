import random
import string


def generate_long_text(filename, length=1000000):
    """
    Generates a long random text file with a specified number of characters.
    The characters are drawn from a-z, A-Z, digits, and some punctuation.
    """
    # Define the character pool
    char_pool = string.ascii_letters + string.digits + string.punctuation + " \n"

    # Generate random text
    long_text = ''.join(random.choices(char_pool, k=length))

    # Write to file
    with open(filename, 'w') as file:
        file.write(long_text)

    print(f"Generated file '{filename}' with {length} characters.")


# Generate a file with 1 million characters
generate_long_text("long_text_test.txt", length=1000000)
