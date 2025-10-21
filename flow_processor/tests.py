from django.test import SimpleTestCase
import os
import tempfile

from .import_service import check_path, read_file, read_files_from_directory


# Create your tests here.
class ImportServiceTests(SimpleTestCase):
    def test_check_path_file_dir_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "a.txt")
            with open(file_path, "w", encoding="utf-8") as fh:
                fh.write("line1\nline2\n")

            self.assertEqual(check_path(tmpdir), "directory")
            self.assertEqual(check_path(file_path), "file")
            self.assertEqual(check_path(os.path.join(tmpdir, "no_such")), "missing")