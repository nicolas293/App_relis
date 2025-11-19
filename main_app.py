import tkinter as tk

class MainApp:
    def __init__(self, root):
        super().__init__()
        self.root = root
        """галавной окно"""
        self.cv = tk.Canvas(self.root, height=430, width=320)
        self.cv.pack(side='left', fill='both')
        """галавной окно"""
        
        self.cv.bind("<Button-1>", self.click_create)
        self.cv.bind("<Button-3>", self.click_del)

        self.root.bind("<ButtonPress-1>" ,self.start_move)
        self.root.bind("<B1-Motion>", self.do_move)

        self.current = 0
        self.colors = ['red', 'green', 'blue', 'yellow', 'orange']
        self.color_index_colors = 0 
        
    def click_create(self, event):
        self.current += 1
        self.config(text=str(self.current))

        self.color_index_colors = (self.color_index_colors + 1) % len(self.colors)
        self.cv.config(bg=self.colors[self.color_index_colors])
    
    def click_del(self, event):
        self.current -= 1
        self.cv.config(text=str(self.current))

        self.color_index_colors = (self.color_index_colors - 1) % len(self.colors)
        self.cv.config(bg=self.colors[self.color_index_colors])
    
    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        dx = event.x - self.x
        dy = event.y - self.y
        x = self.root.winfo_x() + dx
        y = self.root.winfo_y() + dy
        self.root.geometry(f"+{x}+{y}")


if __name__ == '__main__':
    app = tk.Tk()
    app.geometry('430x320')
    app.config(bg='black', bd=3, relief='ridge')
    app.overrideredirect(True)
    app.wm_attributes('-alpha', 0.8)
    app.attributes('-topmost', True)
    app.resizable(0, 0)
    win = MainApp(app)
    app.mainloop()