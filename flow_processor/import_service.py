import os
import argparse
from .file_process_service import process_file


# IMPORTING FILE AND READING

# TODO : Check if File already in db

def check_path(directory_path):
    """Checks if the provided directory path exists."""
    if os.path.isdir(directory_path):
        return "directory"
    if os.path.isfile(directory_path):
        return "file"
    return "missing"

def read_file(file_path):
    """Reads the content of a single file."""

    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    return process_file(file_path)
    

def read_files_from_directory(directory_path):
    """Reads all files from the specified directory and returns their contents."""

    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        raise NotADirectoryError(f"Directory not found: {directory_path}")

    file_contents = {}
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                file_contents[filename] = file.read()
            process_file(file_path)
    return file_contents

    