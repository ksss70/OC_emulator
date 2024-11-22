# tests/test_filesystem.py

import unittest
import zipfile
import os
import sys
import uuid

# Добавляем корневую директорию проекта в sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, parent_dir)

from shell_emulator.filesystem import VirtualFileSystem

class TestVirtualFileSystem(unittest.TestCase):
    def setUp(self):
        """Создаёт тестовый ZIP-архив для файловой системы."""
        unique_id = uuid.uuid4().hex  # Генерация уникального имени файла
        self.zip_path = os.path.join(parent_dir, f'test_vfs_{unique_id}.zip')
        with zipfile.ZipFile(self.zip_path, 'w') as zipf:
            zipf.writestr('file1.txt', 'hello')
            zipf.writestr('file2.txt', 'world')
            zipf.writestr('dir1/file3.txt', 'foo')
            zipf.writestr('dir1/dir2/file4.txt', 'bar')
            zipf.writestr('empty_dir/', '')  # Пустая директория
        self.vfs = VirtualFileSystem(self.zip_path)

    def tearDown(self):
        """Закрывает виртуальную файловую систему и удаляет тестовый ZIP-архив после тестов."""
        if hasattr(self, 'vfs') and self.vfs:
            self.vfs.close()
        if os.path.exists(self.zip_path):
            os.remove(self.zip_path)

    def test_initial_path(self):
        self.assertEqual(self.vfs.get_current_path(), '/')

    def test_list_root(self):
        expected = ['dir1/', 'empty_dir/', 'file1.txt', 'file2.txt']
        self.assertListEqual(self.vfs.list_dir(), sorted(expected))

    def test_change_dir_valid(self):
        success = self.vfs.change_dir('dir1')
        self.assertTrue(success)
        self.assertEqual(self.vfs.get_current_path(), '/dir1')

    def test_change_dir_invalid(self):
        success = self.vfs.change_dir('nonexist')
        self.assertFalse(success)
        self.assertEqual(self.vfs.get_current_path(), '/')

    def test_change_dir_parent(self):
        self.vfs.change_dir('dir1')
        success = self.vfs.change_dir('..')
        self.assertTrue(success)
        self.assertEqual(self.vfs.get_current_path(), '/')

    def test_read_file_valid(self):
        content = self.vfs.read_file('file1.txt')
        self.assertEqual(content, 'hello')

    def test_read_file_invalid(self):
        with self.assertRaises(FileNotFoundError):
            self.vfs.read_file('nonexist.txt')

    def test_list_subdir(self):
        self.vfs.change_dir('dir1')
        expected = ['dir2/', 'file3.txt']
        self.assertListEqual(self.vfs.list_dir(), sorted(expected))

    def test_list_empty_dir(self):
        self.vfs.change_dir('empty_dir')
        expected = []
        self.assertListEqual(self.vfs.list_dir(), expected)

if __name__ == '__main__':
    unittest.main()
