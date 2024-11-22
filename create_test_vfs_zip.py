# create_test_vfs_zip.py

import zipfile
import os


def create_test_vfs_zip(zip_path):
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        # Создаём файлы в корневом каталоге
        zipf.writestr('file1.txt', 'hello\nworld\nhello')
        zipf.writestr('file2.txt', 'foo\nbar\nfoo')

        # Создаём подкаталог dir1 и файл внутри него
        zipf.writestr('dir1/file3.txt', 'apple\nbanana\napple')

        # Создаём пустую директорию empty_dir/
        zipf.writestr('empty_dir/', '')

    print(f"Создан ZIP-архив: {zip_path}")


def main():
    # Определяем путь к ZIP-архиву
    # Убедитесь, что ZIP создаётся в той же директории, что и gui.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    zip_path = os.path.join(script_dir, 'shell_emulator', 'test_vfs.zip')

    # Создаём директорию shell_emulator, если её нет
    os.makedirs(os.path.dirname(zip_path), exist_ok=True)

    # Создаём ZIP-архив
    create_test_vfs_zip(zip_path)


if __name__ == "__main__":
    main()
