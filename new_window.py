import tkinter as tk
from tkinter import colorchooser

class AppWin(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.config(bg='black', bd=3, relief='ridge')
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.wm_attributes('-alpha', 0.5)
        self.geometry('540x420')


        self.close = tk.Button(self, text='X', fg='#ffffff', bg='#1c1c1e', command=self.close_window) # закрытие окна
        self.close.place(y=5, x=505)


        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<B1-Motion>", self.do_move)

        self.canvas = tk.Canvas(self, bg='black')
        self.canvas.pack()
        
        # Настройки по умолчанию
        self.color = "black"
        self.tool = "pen"
        self.brush_size = 5
        
        # Создаем панель инструментов
        self.create_tools()
        
        # Привязываем события мыши
        self.canvas.bind("<B3-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-3>", self.reset)

    def close_window(self):
        self.destroy()

    def create_tools(self):
        # Панель инструментов
        tools_frame = tk.Frame(self)
        tools_frame.pack(side=tk.TOP)
        
        # Кнопки инструментов
        tk.Button(tools_frame, text="Ручка", command=lambda: self.select_tool("pen")).pack(side=tk.LEFT)
        tk.Button(tools_frame, text="Ластик", command=lambda: self.select_tool("eraser")).pack(side=tk.LEFT)
        tk.Button(tools_frame, text="Прямоугольник", command=lambda: self.select_tool("rectangle")).pack(side=tk.LEFT)
        tk.Button(tools_frame, text="Цвет", command=self.choose_color).pack(side=tk.LEFT)
        tk.Button(tools_frame, text="Очистить", command=self.clear_canvas).pack(side=tk.LEFT)

    def select_tool(self, tool):
        self.tool = tool

    def choose_color(self):
        self.color = colorchooser.askcolor()[1]

    def paint(self, event):
        if self.tool == "pen":
            # Рисование линии
            self.canvas.create_line(
                event.x, event.y,
                event.x + 1, event.y + 1,
                fill=self.color,
                width=self.brush_size
            )
        elif self.tool == "rectangle":
            # Рисование прямоугольника
            self.canvas.create_rectangle(
                event.x, event.y,
                event.x + 50, event.y + 30,
                outline=self.color
            )
        elif self.tool == "eraser":
            # Ластик (рисование белым)
            self.canvas.create_line(
                event.x, event.y,
                event.x + 10, event.y + 10,
                fill="white",
                width=self.brush_size * 2
            )

    def reset(self, event):
        pass  # Можно добавить дополнительную логику

    def clear_canvas(self):
        self.canvas.delete("all")


    def start_move(self, event):
        self.x = event.x
        self.y = event.y
        
    def do_move(self, event):
        dx = event.x - self.x
        dy = event.y - self.y
        x = self.winfo_x() + dx
        y = self.winfo_y() + dy
        self.geometry(f"+{x}+{y}")    

if __name__ == '__main__':
    win = AppWin()
    win.geometry('540x420')
    win.resizable(0, 0)