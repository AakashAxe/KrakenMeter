import os
import argparse
from .service import check_path, read_files_from_directory, read_file

parse = argparse.ArgumentParser(description="Import files from a directory")
parse.add_argument('path', type=str, help='Add path to flow files')

args = parse.parse_args()


if __name__ == "__main__":
    path_status = check_path(args.path)
    if path_status == "directory":
        files_data = read_files_from_directory(args.path)
        for filename, content in files_data.items():
            print(f"Filename: {filename}\nContent:\n{content}\n{'-'*40}\n")
    else:
        read_file_content = read_file(args.path)
        print(f"Content of the file {args.path}:\n{read_file_content}\n")






