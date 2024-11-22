import tkinter as tk
from tkinter import scrolledtext

class GUI:
    def __init__(self, emulator):
        """
        Инициализирует GUI.

        :param emulator: Объект Emulator.
        """
        self.emulator = emulator
        self.emulator.gui_callback = self.display_output
        self.root = tk.Tk()
        self.root.title("Эмулятор Shell")

        # Область вывода
        self.output_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=20, state='disabled')
        self.output_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Поле ввода команды
        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(self.root, textvariable=self.input_var)
        self.input_entry.pack(padx=10, pady=(0,10), fill=tk.X)
        self.input_entry.bind('<Return>', self.process_input)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def display_output(self, text):
        """Отображает вывод в области вывода."""
        if text == '<CLEAR>':
            self.output_area.configure(state='normal')
            self.output_area.delete('1.0', tk.END)
            self.output_area.configure(state='disabled')
            return
        self.output_area.configure(state='normal')
        self.output_area.insert(tk.END, text + '\n')
        self.output_area.configure(state='disabled')
        self.output_area.see(tk.END)
        if text == 'Завершение работы эмулятора.':
            self.root.after(100, self.root.destroy)

    def process_input(self, event):
        """Обрабатывает ввод пользователя."""
        command = self.input_var.get()
        self.display_output(f"> {command}")
        self.input_var.set('')
        self.emulator.execute_command(command)

    def run(self):
        """Запускает главный цикл GUI."""
        self.root.mainloop()

    def on_close(self):
        """Обрабатывает закрытие окна."""
        self.root.destroy()