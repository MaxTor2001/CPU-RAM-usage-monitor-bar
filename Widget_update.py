class Configure_widgets:
    def configure_cpu_bar(self):

        r = self.cpu.cpu_percent_return()
        for i in range(self.cpu.cpu_count_logical):
            self.list_label[i].configure(
                text=f"Загрузка {i+1} ядра процессора: {r[i]}%"
            )
            self.list_pbar[i].configure(value=r[i])

        r2 = self.cpu.ram_usage()
        self.ram_lab.configure(
            text=f"использование RAM: {r2[2]}%,\n использовано: {round(r2[3]/1048576)} Мбайт, \n доступно: {round(r2[1]/1048576)} Мбайт"
        )

        self.ram_bar.configure(value=r2[2])

        self.wheel = self.after(
            1000, self.configure_cpu_bar
        )  # Циклический перезапуск функции, количество милисекунд, имя метода

    def configure_win(self):  # Метод для перетаскивания рамки при нажатии кнопки move
        if self.wm_overrideredirect():
            self.overrideredirect(False)
        else:
            self.overrideredirect(True)
        self.update()  # Обновление содержимого окна

    def clear_win(self):
        for i in self.winfo_children():
            i.destroy()

    def configure_minimal_win(self):
        self.bar_one.configure(value=self.cpu.cpu_one_return())
        self.ram_bar.configure(value=self.cpu.ram_usage()[2])
        self.wheel = self.after(1000, self.configure_minimal_win)  # Циклический перезапуск функции, количество милисекунд, имя метода