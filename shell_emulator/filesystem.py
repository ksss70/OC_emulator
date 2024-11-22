# shell_emulator/filesystem.py

import zipfile
import os

class VirtualFileSystem:
    def __init__(self, zip_path):
        if not zipfile.is_zipfile(zip_path):
            raise ValueError(f"{zip_path} не является действительным ZIP-архивом.")
        self.zip_path = zip_path
        self.zip = zipfile.ZipFile(zip_path, 'r')
        self.current_path = '/'  # Корневой каталог
        self.update_file_list()

    def update_file_list(self):
        """Обновляет список файлов и директорий в текущем каталоге."""
        self.file_list = []
        prefix = self.current_path.lstrip('/')  # Удаляем ведущий '/'
        for file in self.zip.namelist():
            if not file.startswith(prefix) or file == prefix:
                continue
            remainder = file[len(prefix):]
            if remainder.startswith('/'):
                remainder = remainder[1:]
            if not remainder:
                # 'file' соответствует текущему каталогу с завершающим '/'
                continue
            if '/' in remainder:
                # Это директория
                dir_name = remainder.split('/', 1)[0]
                dir_entry = dir_name + '/'
                if dir_entry not in self.file_list:
                    self.file_list.append(dir_entry)
            else:
                # Это файл
                if remainder:
                    self.file_list.append(remainder)
        self.file_list.sort()

    def list_dir(self):
        """Возвращает список файлов и директорий в текущем каталоге."""
        return self.file_list.copy()

    def change_dir(self, path):
        """Изменяет текущий каталог."""
        if path == '..':
            if self.current_path != '/':
                # Получаем родительский каталог
                parent = os.path.dirname(self.current_path.rstrip('/'))
                if parent == '':
                    parent = '/'
                elif parent != '/':
                    parent += '/'
                # Если parent == '/', не добавляем '/'
                self.current_path = parent
                self.update_file_list()
            return True
        elif path == '/':
            self.current_path = '/'
            self.update_file_list()
            return True
        else:
            # Изменение на подкаталог
            new_path = os.path.join(self.current_path, path).replace('\\', '/')
            if not new_path.endswith('/'):
                new_path += '/'
            # Проверяем, существует ли директория
            exists = any(file.startswith(new_path.lstrip('/')) for file in self.zip.namelist())
            if exists:
                self.current_path = new_path.rstrip('/')
                self.update_file_list()
                return True
            else:
                return False

    def get_current_path(self):
        """Возвращает текущий путь."""
        return self.current_path if self.current_path != '' else '/'

    def read_file(self, filename):
        """Читает содержимое файла из виртуальной файловой системы."""
        # Формируем полный путь к файлу
        if self.current_path == '/':
            file_path = filename
        else:
            file_path = f"{self.current_path}/{filename}"
        file_path = file_path.replace('\\', '/').lstrip('/')
        if file_path in self.zip.namelist():
            with self.zip.open(file_path) as f:
                return f.read().decode('utf-8')
        else:
            raise FileNotFoundError(f"Файл {filename} не найден в виртуальной файловой системе.")

    def close(self):
        """Закрывает ZIP-архив."""
        self.zip.close()
