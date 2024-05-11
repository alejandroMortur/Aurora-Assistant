def read_file(file_path):
    # Initialize a list to store the lines of the file
    lines = []
    
    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Read each line of the file and add it to the list
        for line in file:
            lines.append(line.strip())  # Remove leading and trailing whitespace from the line
            
    # Concatenate all lines into a single string separated by newline characters
    file_content = '\n'.join(lines)
    
    return file_content

def read_word(file_path):
    words = []

    # Open the file in read mode
    with open(file_path, "r") as f:
        # Read each line of the file
        for line in f:
            # Split the line into words and add them to the list
            words.extend(line.strip().split(','))
            
    return words
