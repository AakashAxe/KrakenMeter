import os
import argparse

def check_path(directory_path):
    """Checks if the provided directory path exists."""
    if os.path.isdir(directory_path):
        return "directory"
    if os.path.isfile(directory_path):
        return "file"
    return "missing"


def read_file(file_path):
    """Reads the content of a single file."""
    with open(file_path, 'r') as file:
        return file.read()

def read_files_from_directory(directory_path):
    """Reads all files from the specified directory and returns their contents."""
    file_contents = {}
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                file_contents[filename] = file.read()
    return file_contents