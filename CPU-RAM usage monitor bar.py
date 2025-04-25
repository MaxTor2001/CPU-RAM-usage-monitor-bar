import tkinter as tk
from tkinter import ttk
import sys
from process import CpuBar
from Widget_update import Configure_widgets


class Application(tk.Tk, Configure_widgets):

    def __init__(self):
        tk.Tk.__init__(self)
        self.attributes("-alpha", 1)  # Прозрачность
        self.attributes("-topmost", True)  # Поверх остальных окон
        self.overrideredirect(True)  # Убрать рамку, не дает закрыть окно
        self.resizable(False, False)  # Не дает растягивать окно
        self.title("CPU-RAM usage monitor bar")  # Название приложения в рамке

        # Set background color
        self.configure(bg="#f5f5f5")

        # Set theme and style
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure(
            "TButton",
            background="#4CAF50",
            foreground="white",
            font=("Arial", 10, "bold"),
        )
        self.style.configure(
            "TLabel", background="#f0f0f0", foreground="#333333", font=("Arial", 10)
        )
        self.style.configure(
            "TLabelFrame",
            background="#e0e0e0",
            foreground="#333333",
            font=("Arial", 10, "bold"),
        )
        self.style.configure(
            "TCombobox", background="#ffffff", foreground="#333333", font=("Arial", 10)
        )
        self.style.configure(
            "TProgressbar", troughcolor="#d3d3d3", background="#4CAF50"
        )

        # self.logo_image = Image.open("D:\work_place\CPU-RAM\logo")
        # self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        # self.logo_label = ttk.Label(self, image=self.logo_photo, background='#f5f5f5')
        # self.logo_label.pack(pady=10)

        self.cpu = CpuBar()  # Запуск класса
        self.run_set_ui()

    def run_set_ui(self):
        self.set_ui()  # Создание окна
        self.make_bar_cpu_usage()  # Заполнение виджетами
        self.configure_cpu_bar()

    def set_ui(self):
        exit_but = ttk.Button(self, text="Exit", command=self.app_exit)
        exit_but.pack(fill=tk.X)

        self.bar2 = ttk.LabelFrame(self, text="Manual")
        self.bar2.pack(fill=tk.X)

        self.combo_win = ttk.Combobox(
            self.bar2, values=["hide", "don't hide", "min"], width=9, state="readonly"
        )
        self.combo_win.current(1)
        self.combo_win.pack(side=tk.LEFT)

        ttk.Button(self.bar2, text="move", command=self.configure_win).pack(
            side=tk.LEFT
        )
        ttk.Button(self.bar2, text=">>>").pack(side=tk.LEFT)

        self.bar = ttk.LabelFrame(self, text="Power")
        self.bar.pack(fill=tk.BOTH)

        self.bind_class("Tk", "<Enter>", self.enter_mouse)
        self.bind_class("Tk", "<Leave>", self.leave_mouse)
        self.combo_win.bind("<<ComboboxSelected>>", self.choice_combo)

    def make_bar_cpu_usage(self):
        ttk.Label(
            self.bar,
            text=f"Physical cores: {self.cpu.cpu_count}, Logical cores: {self.cpu.cpu_count_logical}",
            anchor=tk.CENTER,
        ).pack(fill=tk.X)

        self.list_label = []
        self.list_pbar = []

        for i in range(self.cpu.cpu_count_logical):
            self.list_label.append(ttk.Label(self.bar, anchor=tk.CENTER))
            self.list_pbar.append(ttk.Progressbar(self.bar, length=100))

        for i in range(self.cpu.cpu_count_logical):
            self.list_label[i].pack(fill=tk.X)
            self.list_pbar[i].pack(fill=tk.X)

        self.ram_lab = ttk.Label(self.bar, text="", anchor=tk.CENTER)
        self.ram_lab.pack(fill=tk.X)
        self.ram_bar = ttk.Progressbar(self.bar, length=100)
        self.ram_bar.pack(fill=tk.X)

    def make_minimal_win(self):

        self.bar_one = ttk.Progressbar(self, length=100)
        self.bar_one.pack(side=tk.LEFT)

        self.ram_bar = ttk.Progressbar(self, length=100)
        self.ram_bar.pack(side=tk.LEFT)

        ttk.Button(self, text="full", width=5, command=self.make_full_win).pack(
            side=tk.RIGHT
        )

        ttk.Button(self, text="move", width=5, command=self.configure_win).pack(
            side=tk.RIGHT
        )

        self.update()
        self.configure_minimal_win()

    def enter_mouse(self, event):
        if self.combo_win.current() == 0 or 1:
            self.geometry("")

    def leave_mouse(self, event):
        if self.combo_win.current() == 0:
            self.geometry(f"{self.winfo_width()}x1")

    def choice_combo(self, even):
        if self.combo_win.current() == 2:
            self.enter_mouse("")
            self.unbind_class("Tk", "<Enter>")
            self.unbind_class("Tk", "<Leave>")
            self.combo_win.unbind("<<ComboboxSelected>>")
            self.after_cancel(self.wheel)
            self.clear_win()
            self.update()
            self.make_minimal_win()  # Создаем минимальные виджеты после закрытия большого окна
    
    def make_full_win(self):
        self.after_cancel(self.wheel)
        self.clear_win()
        self.update()
        self.run_set_ui()
        self.enter_mouse('')
        self.combo_win.current(1)

    def app_exit(self):
        self.destroy()
        sys.exit()


if __name__ == "__main__":
    root = Application()
    root.mainloop()
