################################################################

# File: header.py
# Author: Satyam Pandey
# Date: 2023-11-02
# Description: This is a Python script for Header generation.

################################################################

import os
from datetime import datetime

def generate_header(file_path):
    # Extract the filename from the file path
    filename = os.path.basename(file_path)

    # Get the current date 
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    header = f"""
################################################################

# File: {filename}
# Author: Satyam Pandey
# Date: {current_date}
# Description: This is a Python script for...

################################################################

""".lstrip()
    return header

def file_contains_header(file_path):
    with open(file_path, 'r') as file:
        for _ in range(3):
        # for line in file:
            line = next(file).strip()
            if line.strip().startswith("# File:"):
                return True
    return False

def add_header_to_files(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".py"):
                file_path = os.path.join(dirpath, filename)
                
                # Check if the file already contains a header
                if not file_contains_header(file_path):
                    header = generate_header(file_path)
                    with open(file_path, 'r') as original:
                        content = original.read()
                    with open(file_path, 'w') as modified:
                        modified.write(header + content)

if __name__ == "__main__":
    project_root = "./"
    add_header_to_files(project_root)

