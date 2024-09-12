import unittest
import os
import shutil
import tempfile
from src.copy_static import clear_and_copy, recursive_copy

class TestFileCopy(unittest.TestCase):

    def setUp(self):
        # Create a temporary source directory
        self.src_dir = tempfile.mkdtemp()

        # Create a temporary destination directory
        self.dest_dir = tempfile.mkdtemp()

        # Populate source directory with some files and subdirectories
        self.create_sample_files()

    def tearDown(self):
        # Remove temporary directories after each test
        shutil.rmtree(self.src_dir)
        shutil.rmtree(self.dest_dir)

    def create_sample_files(self):
        """Helper method to create sample files and directories in the source directory."""
        # Create a sample file in the root of the source directory
        with open(os.path.join(self.src_dir, 'file1.txt'), 'w') as f:
            f.write('This is file 1.')

        # Create a subdirectory
        os.mkdir(os.path.join(self.src_dir, 'subdir'))

        # Create a file inside the subdirectory
        with open(os.path.join(self.src_dir, 'subdir', 'file2.txt'), 'w') as f:
            f.write('This is file 2.')

    def test_recursive_copy(self):
        """Test that recursive_copy copies all files and directories correctly."""
        recursive_copy(self.src_dir, self.dest_dir)

        # Verify that the files have been copied
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, 'file1.txt')))
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, 'subdir', 'file2.txt')))

        # Verify the content of the copied files
        with open(os.path.join(self.dest_dir, 'file1.txt'), 'r') as f:
            self.assertEqual(f.read(), 'This is file 1.')

        with open(os.path.join(self.dest_dir, 'subdir', 'file2.txt'), 'r') as f:
            self.assertEqual(f.read(), 'This is file 2.')

    def test_clear_and_copy(self):
        """Test that clear_and_copy removes all files in the destination before copying."""
        # Create a file in the destination directory before copying
        with open(os.path.join(self.dest_dir, 'old_file.txt'), 'w') as f:
            f.write('This should be deleted.')

        # Run clear_and_copy to clear destination and copy the source
        clear_and_copy(self.src_dir, self.dest_dir)

        # Verify that the old file has been deleted
        self.assertFalse(os.path.exists(os.path.join(self.dest_dir, 'old_file.txt')))

        # Verify that the source files have been copied
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, 'file1.txt')))
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, 'subdir', 'file2.txt')))

        # Verify the content of the copied files
        with open(os.path.join(self.dest_dir, 'file1.txt'), 'r') as f:
            self.assertEqual(f.read(), 'This is file 1.')

        with open(os.path.join(self.dest_dir, 'subdir', 'file2.txt'), 'r') as f:
            self.assertEqual(f.read(), 'This is file 2.')

if __name__ == '__main__':
    unittest.main()
