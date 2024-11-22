# shell_emulator/emulator.py

class Emulator:
    def __init__(self, vfs, gui_callback=None):
        """
        Инициализирует эмулятор.

        :param vfs: Объект VirtualFileSystem.
        :param gui_callback: Функция обратного вызова для отображения вывода в GUI.
        """
        self.vfs = vfs
        self.running = True
        self.gui_callback = gui_callback
        self.last_output = ''  # Хранит последний вывод команды
        self.commands = {
            'ls': self.ls,
            'cd': self.cd,
            'exit': self.exit,
            'uniq': self.uniq,
            'clear': self.clear
        }

    def execute_command(self, command_line):
        """Обрабатывает и выполняет команду."""
        if not self.running:
            return
        parts = command_line.strip().split()
        if not parts:
            return
        cmd = parts[0]
        args = parts[1:]
        if cmd in self.commands:
            try:
                self.commands[cmd](args)
            except Exception as e:
                if self.gui_callback:
                    self.gui_callback(f"Ошибка: {str(e)}")
        else:
            if self.gui_callback:
                self.gui_callback(f"Неизвестная команда: {cmd}")

    def ls(self, args):
        """Команда ls: выводит список файлов и директорий."""
        files = self.vfs.list_dir()
        output = '\n'.join(files)
        self.last_output = output
        if self.gui_callback:
            self.gui_callback(output)

    def cd(self, args):
        """Команда cd: изменяет текущий каталог."""
        if len(args) != 1:
            if self.gui_callback:
                self.gui_callback("Команда cd требует ровно один аргумент.")
            return
        path = args[0]
        success = self.vfs.change_dir(path)
        current_path = self.vfs.get_current_path()
        if success:
            output = f"Текущий каталог: {current_path}"
            self.last_output = output
            if self.gui_callback:
                self.gui_callback(output)
        else:
            output = f"Директория не найдена: {path}"
            if self.gui_callback:
                self.gui_callback(output)

    def exit(self, args):
        """Команда exit: завершает работу эмулятора."""
        self.running = False
        output = "Завершение работы эмулятора."
        if self.gui_callback:
            self.gui_callback(output)
        self.last_output = output

    def uniq(self, args):
        """Команда uniq: удаляет повторяющиеся строки из последнего вывода."""
        if not self.last_output:
            output = "Нечего обрабатывать командой uniq."
            if self.gui_callback:
                self.gui_callback(output)
            return
        last_output = self.last_output
        lines = last_output.splitlines()
        unique_lines = []
        seen = set()
        for line in lines:
            if line not in seen:
                unique_lines.append(line)
                seen.add(line)
        uniq_output = '\n'.join(unique_lines)
        if uniq_output != last_output:
            self.last_output = uniq_output
            if self.gui_callback:
                self.gui_callback(uniq_output)
        # Если uniq_output == last_output, ничего не делаем

    def clear(self, args):
        """Команда clear: очищает экран в GUI."""
        if self.gui_callback:
            self.gui_callback('<CLEAR>')
        self.last_output = ''

    def close(self):
        """Закрывает виртуальную файловую систему."""
        self.vfs.close()
