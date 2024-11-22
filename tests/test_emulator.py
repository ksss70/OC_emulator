import unittest
from filesystem import VirtualFileSystem
from emulator import Emulator
import zipfile
import os

class TestEmulator(unittest.TestCase):
    def setUp(self):
        """Создает тестовый ZIP-архив и инициализирует эмулятор."""
        self.zip_path = 'test_vfs.zip'
        with zipfile.ZipFile(self.zip_path, 'w') as zipf:
            zipf.writestr('file1.txt', 'hello\nworld\nhello')
            zipf.writestr('file2.txt', 'foo\nbar\nfoo')
            zipf.writestr('dir1/file3.txt', 'apple\nbanana\napple')
        self.vfs = VirtualFileSystem(self.zip_path)
        self.output = []
        self.emulator = Emulator(self.vfs, gui_callback=self.mock_gui_callback)

    def mock_gui_callback(self, text):
        """Фиктивная функция обратного вызова для захвата вывода."""
        self.output.append(text)

    def tearDown(self):
        """Удаляет тестовый ZIP-архив после тестов."""
        if os.path.exists(self.zip_path):
            os.remove(self.zip_path)

    # Тесты для команды ls
    def test_ls_root(self):
        self.emulator.execute_command('ls')
        expected = 'dir1/\nfile1.txt\nfile2.txt'
        self.assertIn(expected, self.output)

    def test_ls_subdir(self):
        self.emulator.execute_command('cd dir1')
        self.emulator.execute_command('ls')
        expected = 'file3.txt'
        self.assertIn(expected, self.output)

    def test_ls_empty_dir(self):
        # Добавляем пустую директорию
        with zipfile.ZipFile(self.zip_path, 'a') as zipf:
            zipf.writestr('empty_dir/', '')
        self.emulator.execute_command('ls')
        self.assertIn('empty_dir/', self.output)

    # Тесты для команды cd
    def test_cd_valid(self):
        self.emulator.execute_command('cd dir1')
        self.assertIn('Текущий каталог: /dir1/', self.output)

    def test_cd_invalid(self):
        self.emulator.execute_command('cd nonexist')
        self.assertIn('Директория не найдена: nonexist', self.output)

    def test_cd_parent(self):
        self.emulator.execute_command('cd dir1')
        self.emulator.execute_command('cd ..')
        self.assertIn('Текущий каталог: /', self.output)

    # Тесты для команды uniq
    def test_uniq_no_previous_output(self):
        self.emulator.execute_command('uniq')
        self.assertIn('Нечего обрабатывать командой uniq.', self.output)

    def test_uniq_with_duplicates(self):
        self.emulator.execute_command('ls')
        self.emulator.execute_command('uniq')
        expected = 'dir1/\nfile1.txt\nfile2.txt'
        self.assertIn(expected, self.output)

    def test_uniq_remove_duplicates(self):
        self.emulator.execute_command('ls')
        self.emulator.execute_command('uniq')
        self.emulator.execute_command('uniq')
        # uniq не должен добавить дубликаты
        self.assertEqual(self.output.count('dir1/\nfile1.txt\nfile2.txt'), 1)

    # Тесты для команды clear
    def test_clear(self):
        self.emulator.execute_command('ls')
        self.emulator.execute_command('clear')
        self.assertIn('<CLEAR>', self.output)

    def test_clear_then_ls(self):
        self.emulator.execute_command('ls')
        self.emulator.execute_command('clear')
        self.emulator.execute_command('ls')
        expected = 'dir1/\nfile1.txt\nfile2.txt'
        self.assertIn('<CLEAR>', self.output)
        self.assertIn(expected, self.output)

    # Тесты для команды exit
    def test_exit(self):
        self.emulator.execute_command('exit')
        self.assertFalse(self.emulator.running)
        self.assertIn('Завершение работы эмулятора.', self.output)

    def test_exit_with_args(self):
        self.emulator.execute_command('exit now')
        self.assertFalse(self.emulator.running)
        self.assertIn('Завершение работы эмулятора.', self.output)

    # Тесты для неизвестной команды
    def test_unknown_command(self):
        self.emulator.execute_command('foo')
        self.assertIn('Неизвестная команда: foo', self.output)

if __name__ == '__main__':
    unittest.main()