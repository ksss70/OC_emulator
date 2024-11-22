import argparse
import sys
from filesystem import VirtualFileSystem
from emulator import Emulator
from gui import GUI

def parse_arguments():
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(description="Эмулятор Shell с GUI")
    parser.add_argument('zip_path', help="Путь к ZIP-архиву виртуальной файловой системы.")
    parser.add_argument('startup_script', nargs='?', help="Путь к стартовому скрипту.")
    return parser.parse_args()

def execute_startup_script(emulator, script_path):
    """Выполняет команды из стартового скрипта."""
    try:
        with open(script_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    emulator.execute_command(line)
    except Exception as e:
        print(f"Ошибка при выполнении стартового скрипта: {e}")

def main():
    args = parse_arguments()
    try:
        vfs = VirtualFileSystem(args.zip_path)
    except Exception as e:
        print(f"Не удалось инициализировать виртуальную файловую систему: {e}")
        sys.exit(1)

    emulator = Emulator(vfs)

    if args.startup_script:
        execute_startup_script(emulator, args.startup_script)

    gui = GUI(emulator)
    gui.run()

if __name__ == '__main__':
    main()