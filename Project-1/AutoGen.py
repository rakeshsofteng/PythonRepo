def read_text_file(file_path):
    """Reads and returns the content of a text file at the given path."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_text_file(file_path, data):
    """Writes the given data to a text file at the given path."""
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(data)
        
        
input_path = r"C:\DATA\RK\Python\Project-1\RAKA1\input.txt"
output_path = r"C:\DATA\RK\Python\Project-1\RAKA1\output.txt"

            # Read content from input file
content = read_text_file(input_path)
#print("Read content:", content)
           
            # Write content to output file
write_text_file(output_path, content)
#print(f"Content written to {output_path}")

# if __name__ == "__main__":
#  print("__name__ if section"+__name__)
# else:
#     print("__name__ is not __main__"+ __name__)
         
        