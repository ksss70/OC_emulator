import tkinter as tk
from tkinter import scrolledtext
import threading
import os

# Импортируем ваши классы VirtualFileSystem и Emulator
from filesystem import VirtualFileSystem
from emulator import Emulator

class ShellGUI:
    def __init__(self, root, emulator):
        self.root = root
        self.emulator = emulator
        self.emulator.gui_callback = self.update_output  # Связываем callback

        # Настройка окна
        self.root.title("Shell Emulator")
        self.root.geometry("800x600")

        # Создаём текстовое поле для вывода
        self.output_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled', font=("Consolas", 12))
        self.output_area.pack(expand=True, fill='both', padx=10, pady=10)

        # Создаём фрейм для строки ввода
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill='x', padx=10, pady=5)

        # Метка для ввода
        self.input_label = tk.Label(input_frame, text=">> ", font=("Consolas", 12))
        self.input_label.pack(side='left')

        # Строка ввода
        self.input_entry = tk.Entry(input_frame, font=("Consolas", 12))
        self.input_entry.pack(side='left', fill='x', expand=True)
        self.input_entry.bind("<Return>", self.handle_command)  # Обработка нажатия Enter

        # Инициализируем поток для обработки команд
        self.command_thread = threading.Thread(target=self.process_commands, daemon=True)
        self.command_thread.start()

    def update_output(self, text):
        """Функция обратного вызова для обновления текстового поля."""
        self.output_area.configure(state='normal')
        self.output_area.insert(tk.END, text + "\n")
        self.output_area.configure(state='disabled')
        self.output_area.see(tk.END)  # Прокрутка вниз

    def handle_command(self, event):
        """Обработка ввода команды пользователем."""
        command = self.input_entry.get()
        self.input_entry.delete(0, tk.END)  # Очищаем строку ввода

        if command.strip() == "":
            return  # Игнорируем пустые команды

        # Добавляем команду в вывод с префиксом
        self.update_output(f">> {command}")

        # Отправляем команду эмулятору
        self.emulator.execute_command(command)

    def process_commands(self):
        """Дополнительный поток для обработки команд, если необходимо."""
        # В текущей реализации не требуется, но можно расширить функциональность
        pass


def main():
    # Определяем абсолютный путь к ZIP-архиву
    script_dir = os.path.dirname(os.path.abspath(__file__))
    zip_path = os.path.join(script_dir, 'test_vfs.zip')

    # Создаём экземпляр VirtualFileSystem
    vfs = VirtualFileSystem(zip_path)

    # Создаём экземпляр Emulator
    emulator = Emulator(vfs)

    # Создаём главное окно
    root = tk.Tk()

    # Создаём GUI для оболочки
    gui = ShellGUI(root, emulator)

    # Запускаем главный цикл Tkinter
    root.mainloop()

    # Закрываем эмулятор после закрытия GUI
    emulator.close()

if __name__ == "__main__":
    main()