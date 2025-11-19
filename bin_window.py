import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class TrashItem:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.file_size = os.path.getsize(file_path)

class TrashBin:
    def __init__(self):
        self.items = []
    
    def add_item(self, file_path):
        if os.path.exists(file_path):
            self.items.append(TrashItem(file_path))
            return True
        return False
    
    def remove_item(self, file_path):
        self.items = [item for item in self.items if item.file_path != file_path]
    
    def clear_all(self):
        self.items = []

class TrashApp(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Корзина для мусора")
        self.geometry("600x400")
        self.trashed_files = TrashBin()

        self.config(bg='black', bd=3, relief='ridge')
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.wm_attributes('-alpha', 0.7)
        self.resizable(0, 0)

        self.create_widgets()
        self.update_list()

        self.update_idletasks()
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"+{x}+{y}")  

        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<B1-Motion>", self.do_move)

        self.close = tk.Button(self, text='X', fg='#ffffff', bg='#1c1c1e', command=self.close_bin) # закрытие окна
        self.close.place(y=5, x=569)

    def close_bin(self):
        self.destroy()

    def start_move(self, event):
        self.x = event.x
        self.y = event.y
        
    def do_move(self, event):
        dx = event.x - self.x
        dy = event.y - self.y
        x = self.winfo_x() + dx
        y = self.winfo_y() + dy
        self.geometry(f"+{x}+{y}") 


    def create_widgets(self):
        # Основная рамка
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Список файлов
        self.listbox = tk.Listbox(main_frame, width=50, height=15)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Кнопки управления
        button_frame = ttk.Frame(self, padding=10)
        button_frame.pack(fill=tk.X)

        ttk.Button(button_frame, text="Добавить файл", command=self.add_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Удалить выбранный", command=self.remove_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Очистить корзину", command=self.clear_all).pack(side=tk.LEFT, padx=5)

    def add_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            if self.trashed_files.add_item(file_path):
                self.update_list()
            else:
                messagebox.showerror("Ошибка", "Файл не существует")

    def remove_selected(self):
        try:
            selected_index = self.listbox.curselection()[0]
            file_path = self.trashed_files.items[selected_index].file_path
            self.trashed_files.remove_item(file_path)
            self.update_list()
        except IndexError:
            messagebox.showwarning("Предупреждение", "Выберите файл для удаления")

    def clear_all(self):
        confirm = messagebox.askyesno("Подтверждение", "Вы действительно хотите очистить корзину?")
        if confirm:
            self.trashed_files.clear_all()
            self.update_list()

    def update_list(self):
        self.listbox.delete(0, tk.END)
        for item in self.trashed_files.items:
            self.listbox.insert(tk.END, f"{item.file_name} ({item.file_size} байт)")

if __name__ == "__main__":
    app = TrashApp()
