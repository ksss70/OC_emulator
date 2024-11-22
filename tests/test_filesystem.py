import unittest
from filesystem import VirtualFileSystem
import zipfile
import os

class TestVirtualFileSystem(unittest.TestCase):
    def setUp(self):
        """Создает тестовый ZIP-архив для файловой системы."""
        self.zip_path = 'test_vfs.zip'
        with zipfile.ZipFile(self.zip_path, 'w') as zipf:
            zipf.writestr('file1.txt', 'hello')
            zipf.writestr('dir1/file2.txt', 'world')
            zipf.writestr('dir1/dir2/file3.txt', '!')
            zipf.writestr('dir3/', '')  # Пустая директория

    def tearDown(self):
        """Удаляет тестовый ZIP-архив после тестов."""
        if os.path.exists(self.zip_path):
            os.remove(self.zip_path)

    def test_initial_path(self):
        vfs = VirtualFileSystem(self.zip_path)
        self.assertEqual(vfs.get_current_path(), '/')

    def test_list_root(self):
        vfs = VirtualFileSystem(self.zip_path)
        expected = ['dir1/', 'dir3/', 'file1.txt']
        self.assertListEqual(vfs.list_dir(), sorted(expected))

    def test_change_dir_valid(self):
        vfs = VirtualFileSystem(self.zip_path)
        success = vfs.change_dir('dir1')
        self.assertTrue(success)
        self.assertEqual(vfs.get_current_path(), '/dir1/')

    def test_change_dir_invalid(self):
        vfs = VirtualFileSystem(self.zip_path)
        success = vfs.change_dir('nonexist')
        self.assertFalse(success)
        self.assertEqual(vfs.get_current_path(), '/')

    def test_change_dir_parent(self):
        vfs = VirtualFileSystem(self.zip_path)
        vfs.change_dir('dir1')
        success = vfs.change_dir('..')
        self.assertTrue(success)
        self.assertEqual(vfs.get_current_path(), '/')

    def test_read_file_valid(self):
        vfs = VirtualFileSystem(self.zip_path)
        content = vfs.read_file('file1.txt')
        self.assertEqual(content, 'hello')

    def test_read_file_invalid(self):
        vfs = VirtualFileSystem(self.zip_path)
        with self.assertRaises(FileNotFoundError):
            vfs.read_file('nonexist.txt')

    def test_list_subdir(self):
        vfs = VirtualFileSystem(self.zip_path)
        vfs.change_dir('dir1')
        expected = ['dir2/', 'file2.txt']
        self.assertListEqual(vfs.list_dir(), sorted(expected))

    def test_list_empty_dir(self):
        vfs = VirtualFileSystem(self.zip_path)
        vfs.change_dir('dir3')
        expected = []
        self.assertListEqual(vfs.list_dir(), expected)

if __name__ == '__main__':
    unittest.main()