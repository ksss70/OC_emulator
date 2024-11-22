# tests/test_emulator.py

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
from shell_emulator.emulator import Emulator

class TestEmulator(unittest.TestCase):
    def setUp(self):
        """Создаёт тестовый ZIP-архив и инициализирует эмулятор."""
        unique_id = uuid.uuid4().hex  # Генерация уникального имени файла
        self.zip_path = os.path.join(parent_dir, f'test_vfs_{unique_id}.zip')
        with zipfile.ZipFile(self.zip_path, 'w') as zipf:
            zipf.writestr('file1.txt', 'hello\nworld\nhello')
            zipf.writestr('file2.txt', 'foo\nbar\nfoo')
            zipf.writestr('dir1/file3.txt', 'apple\nbanana\napple')
            zipf.writestr('empty_dir/', '')  # Добавляем пустую директорию
        self.vfs = VirtualFileSystem(self.zip_path)
        self.output = []
        self.emulator = Emulator(self.vfs, gui_callback=self.mock_gui_callback)

    def tearDown(self):
        """Закрывает эмулятор и удаляет тестовый ZIP-архив после тестов."""
        if self.emulator:
            self.emulator.close()
        if os.path.exists(self.zip_path):
            os.remove(self.zip_path)

    def mock_gui_callback(self, text):
        """Фиктивная функция обратного вызова для захвата вывода."""
        self.output.append(text)

    # Тесты для команды ls
    def test_ls_root(self):
        self.emulator.execute_command('ls')
        expected = 'dir1/\nempty_dir/\nfile1.txt\nfile2.txt'
        self.assertIn(expected, self.output[-1])

    def test_ls_subdir(self):
        self.emulator.execute_command('cd dir1')
        self.emulator.execute_command('ls')
        expected = 'file3.txt'
        self.assertIn(expected, self.output[-1])

    def test_ls_empty_dir(self):
        # Пустая директория уже добавлена в setUp
        self.emulator.execute_command('ls')
        self.assertIn('empty_dir/', self.output[-1])

    # Тесты для команды cd
    def test_cd_valid(self):
        self.emulator.execute_command('cd dir1')
        self.assertIn('Текущий каталог: /dir1', self.output[-1])

    def test_cd_invalid(self):
        self.emulator.execute_command('cd nonexist')
        self.assertIn('Директория не найдена: nonexist', self.output[-1])

    def test_cd_parent(self):
        self.emulator.execute_command('cd dir1')
        self.emulator.execute_command('cd ..')
        self.assertIn('Текущий каталог: /', self.output[-1])

    # Тесты для команды uniq
    def test_uniq_no_previous_output(self):
        self.emulator.execute_command('uniq')
        self.assertIn('Нечего обрабатывать командой uniq.', self.output[-1])

    def test_uniq_with_duplicates(self):
        self.emulator.execute_command('ls')
        self.emulator.execute_command('uniq')
        expected = 'dir1/\nempty_dir/\nfile1.txt\nfile2.txt'
        self.assertIn(expected, self.output[-1])

    def test_uniq_remove_duplicates(self):
        self.emulator.execute_command('ls')
        self.emulator.execute_command('uniq')
        self.emulator.execute_command('uniq')  # Повторный вызов uniq
        # uniq не должен добавить дубликаты
        expected = 'dir1/\nempty_dir/\nfile1.txt\nfile2.txt'
        count = self.output.count(expected)
        self.assertEqual(count, 1)

    # Тесты для команды clear
    def test_clear(self):
        self.emulator.execute_command('ls')
        self.emulator.execute_command('clear')
        self.assertIn('<CLEAR>', self.output[-1])

    def test_clear_then_ls(self):
        self.emulator.execute_command('ls')
        self.emulator.execute_command('clear')
        self.emulator.execute_command('ls')
        expected = 'dir1/\nempty_dir/\nfile1.txt\nfile2.txt'
        self.assertIn('<CLEAR>', self.output[-2])  # '<CLEAR>' до второго 'ls'
        self.assertIn(expected, self.output[-1])

    # Тесты для команды exit
    def test_exit(self):
        self.emulator.execute_command('exit')
        self.assertFalse(self.emulator.running)
        self.assertIn('Завершение работы эмулятора.', self.output[-1])

    def test_exit_with_args(self):
        self.emulator.execute_command('exit now')
        self.assertFalse(self.emulator.running)
        self.assertIn('Завершение работы эмулятора.', self.output[-1])

    # Тесты для неизвестной команды
    def test_unknown_command(self):
        self.emulator.execute_command('foo')
        self.assertIn('Неизвестная команда: foo', self.output[-1])

if __name__ == '__main__':
    unittest.main()
