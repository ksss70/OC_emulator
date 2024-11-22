import zipfile
import os

class VirtualFileSystem:
    def __init__(self, zip_path):
        if not zipfile.is_zipfile(zip_path):
            raise ValueError(f"{zip_path} не является действительным ZIP-архивом.")
        self.zip_path = zip_path
        self.zip = zipfile.ZipFile(zip_path, 'r')
        self.current_path = '/'
        self.update_file_list()

    def update_file_list(self):
        """Обновляет список файлов и директорий в текущем каталоге."""
        self.file_list = []
        path_len = len(self.current_path)
        for file in self.zip.namelist():
            if file.startswith(self.current_path) and file != self.current_path:
                remainder = file[path_len:]
                if '/' in remainder:
                    # Это директория
                    dir_name = remainder.split('/', 1)[0]
                    if dir_name + '/' not in self.file_list:
                        self.file_list.append(dir_name + '/')
                else:
                    # Это файл
                    self.file_list.append(remainder)
        self.file_list.sort()

    def list_dir(self):
        """Возвращает список файлов и директорий в текущем каталоге."""
        return self.file_list

    def change_dir(self, path):
        """Изменяет текущий каталог."""
        if path == '..':
            if self.current_path != '/':
                self.current_path = os.path.dirname(self.current_path.rstrip('/')) + '/'
                self.update_file_list()
            return True
        elif path == '/':
            self.current_path = '/'
            self.update_file_list()
            return True
        else:
            new_path = os.path.join(self.current_path, path)
            if not new_path.endswith('/'):
                new_path += '/'
            # Проверяем, существует ли директория
            for file in self.zip.namelist():
                if file.startswith(new_path):
                    self.current_path = new_path
                    self.update_file_list()
                    return True
            return False

    def get_current_path(self):
        """Возвращает текущий путь."""
        return self.current_path

    def read_file(self, filename):
        """Читает содержимое файла из виртуальной файловой системы."""
        file_path = os.path.join(self.current_path, filename)
        if file_path in self.zip.namelist():
            with self.zip.open(file_path) as f:
                return f.read().decode('utf-8')
        else:
            raise FileNotFoundError(f"Файл {filename} не найден в виртуальной файловой системе.")