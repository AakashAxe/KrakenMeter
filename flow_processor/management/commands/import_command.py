import argparse
from django.core.management.base import BaseCommand, CommandError
from flow_processor.import_service import check_path, read_files_from_directory, read_file

class Command(BaseCommand):
    help = 'Imports Meter Flow files from a specified file'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=argparse.FileType('r'))

    def handle(self, *args, **options):
        filename = options['filename']
        print(filename)
        self.stdout.write(f"Processing file: {filename.name}")
        file = filename.name
        path_status = check_path(filename.name)
        if path_status == "directory":
            files_data = read_files_from_directory(file)
            for filename, content in files_data.items():
                print(f"Filename: {filename}\nContent:\n{content}\n{'-'*40}\n")
        elif path_status == "file":
            read_file_content = read_file(file)
            print(f"Content of the file {file}:\n{read_file_content}\n")
        else:
            print(f"The path {file} does not exist.")
        