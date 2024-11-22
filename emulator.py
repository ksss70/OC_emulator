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
        self.output = []
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
                result = self.commands[cmd](args)
                if result:
                    self.output.append(result)
                    if self.gui_callback:
                        self.gui_callback(result)
            except Exception as e:
                if self.gui_callback:
                    self.gui_callback(f"Ошибка: {str(e)}")
        else:
            if self.gui_callback:
                self.gui_callback(f"Неизвестная команда: {cmd}")

    def ls(self, args):
        """Команда ls: выводит список файлов и директорий."""
        files = self.vfs.list_dir()
        return '\n'.join(files)

    def cd(self, args):
        """Команда cd: изменяет текущий каталог."""
        if len(args) != 1:
            return "Команда cd требует ровно один аргумент."
        path = args[0]
        success = self.vfs.change_dir(path)
        if success:
            return f"Текущий каталог: {self.vfs.get_current_path()}"
        else:
            return f"Директория не найдена: {path}"

    def exit(self, args):
        """Команда exit: завершает работу эмулятора."""
        self.running = False
        if self.gui_callback:
            self.gui_callback("Завершение работы эмулятора.")
        return "Завершение работы эмулятора."

    def uniq(self, args):
        """Команда uniq: удаляет повторяющиеся строки из последнего вывода."""
        if not self.output:
            return "Нечего обрабатывать командой uniq."
        last_output = self.output[-1]
        lines = last_output.splitlines()
        unique_lines = []
        seen = set()
        for line in lines:
            if line not in seen:
                unique_lines.append(line)
                seen.add(line)
        uniq_output = '\n'.join(unique_lines)
        self.output.append(uniq_output)
        return uniq_output

    def clear(self, args):
        """Команда clear: очищает экран в GUI."""
        if self.gui_callback:
            self.gui_callback('<CLEAR>')
        self.output = []
        return ''