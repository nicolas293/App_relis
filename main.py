import os
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from new_window import AppWin
from bin_window import TrashApp
from themeapp import Themes


class DelayedApp:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()  # Скрываем основное окно

        # Создаем временное окно загрузки
        self.loading_window = tk.Toplevel()
        self.loading_window.title("Загрузка...")
        self.loading_window.geometry("420x230")
        self.loading_window.config(bg='black', bd=3, relief='ridge')
        self.loading_window.overrideredirect(True)
        self.loading_window.attributes('-topmost', True)
        self.loading_window.wm_attributes('-alpha', 0.7)
        
        # Загружаем и обрабатываем изображение
        self.image = Image.open("img/new_start.jpg")
        # Изменяем размер изображения под окно
        self.image = self.image.resize((420, 230))
        self.bg_image = ImageTk.PhotoImage(self.image)

        # Создаем метку для отображения изображения
        self.label_img_start = tk.Label(self.loading_window, image=self.bg_image)
        self.label_img_start.image = self.bg_image  # Сохраняем ссылку на изображение
        self.label_img_start.place(x=0, y=0, relwidth=1, relheight=1)

        # Добавляем текст загрузки
        self.label = tk.Label(
            self.loading_window, 
            text="Пожалуйста, подождите.....",
            font=("Arial", 12)
        )
        self.label.pack(pady=75)

        self.loading_window.update_idletasks()
        width = self.loading_window.winfo_reqwidth()
        height = self.loading_window.winfo_reqheight()
        x = (self.loading_window.winfo_screenwidth() - width) // 2
        y = (self.loading_window.winfo_screenheight() - height) // 2
        self.loading_window.geometry(f"+{x}+{y}")
        
        # Задержка в 4 секунды (4000 миллисекунд)
        self.loading_window.after(4000, self.start_main_app)
        
    def start_main_app(self):
        # Закрываем окно загрузки
        self.loading_window.destroy()
        
        # Показываем основное окно
        self.root.deiconify()

        # Инициализация менеджера тем
        self.theme_manager = Themes()
        
        # Применение начальной темы
        self.apply_theme()
        
        # Создаем элементы интерфейса
        # Загружаем и обрабатываем изображение

        self.background_label = tk.Label(self.root)
        self.background_label.pack(side='left', fill='both')

        self.panel_menu = tk.Frame(self.root, height=402, width=43, relief='ridge', bd=1, bg="#303031") # панель иконок
        self.panel_menu.place(y=5, x=5)

        self.photo_1 = Image.open('icon/colorpaletre.png')
        self.photo_2 = Image.open('icon/bindelete.png')

        self.img_1 = ImageTk.PhotoImage(self.photo_1)
        self.img_2 = ImageTk.PhotoImage(self.photo_2)

        self.icon_1 = tk.Button(self.panel_menu, image=self.img_1, command=AppWin)
        self.icon_2 = tk.Button(self.panel_menu, image=self.img_2, command=TrashApp)

        self.icon_1.place(y=50, x=3)
        self.icon_2.place(y=362, x=3)

        self.photo = PhotoImage(file='icon/Registr.png')
        
        self.btn = tk.Button(self.root, compound=CENTER, fg='#ffffff', bg='#1c1c1e', text=' ', 
                             image=self.photo, command=lambda:(self.menu_label())) # кнопка меню
        self.btn.place(y=5, x=7)

        self.close = tk.Button(self.root, text='X', fg='#ffffff', bg='#1c1c1e', command=quit) # закрытие окна
        self.close.place(y=5, x=505)

        self.label = tk.Label(self.root, bg='#1c1c1e', relief='ridge', bd=3, height=20, width=30) # окно меню

        self.btn_fon = tk.Button(self.label, text="Сменить тему", command=self.change_theme)
        self.btn_fon.place(y=5, x=5)

        # Кнопка добавления нового изображения
        self.btn = tk.Button(self.label, text="Добавить изображение", command=self.open_image)
        self.btn.place(y=38, x=5)

        self.root.bind("<ButtonPress-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.do_move)

        self.alpha = 0.0
        self.step = 0.05

        self.root.update_idletasks()
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"+{x}+{y}")

    def menu_label(self):
        if self.label.winfo_ismapped():
            self.label.place_forget()
        else:
            self.label.place(y=42, x=50)   

    def start_move(self, event):
        self.x = event.x
        self.y = event.y
        
    def do_move(self, event):
        dx = event.x - self.x
        dy = event.y - self.y
        x = self.root.winfo_x() + dx
        y = self.root.winfo_y() + dy
        self.root.geometry(f"+{x}+{y}")            
    

    def apply_theme(self):
        # Применение темы к корневому окну
        self.theme_manager.apply_theme(self.root)
        
        # Применение темы ко всем виджетам
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                self.theme_manager.apply_button_theme(widget)
            else:
                self.theme_manager.apply_theme(widget)

    def change_theme(self):
        # Переключение между темами
        if self.theme_manager.current_theme == "light":
            self.theme_manager.set_theme("dark")
        else:
            self.theme_manager.set_theme("light")
            
        # Применение новой темы
        self.apply_theme()

    def open_image(self):
        # Открываем диалоговое окно для выбора файла
        filetypes = (("Изображения", "*.jpg *.jpeg *.png *.gif"),
                    ("Все файлы", "*.*"))
        filename = filedialog.askopenfilename(
            title="Выбрать изображение",
            filetypes=filetypes,
            initialdir="/"
        )
        
        if filename:
            # Загружаем и отображаем изображение как фон
            self.set_background(filename)

    def set_background(self, path):
        try:
            # Открываем изображение
            image = Image.open(path)
            # Конвертируем в формат Tkinter
            self.tk_image = ImageTk.PhotoImage(image)
            # Обновляем фон
            self.background_label.config(image=self.tk_image)
            self.background_label.image = self.tk_image  # Сохраняем ссылку
        except Exception as e:
            print(f"Ошибка при загрузке изображения: {e}")
    
    def set_background(self, path):
        try:
            image = Image.open(path)
            # Масштабируем под размер окна
            image = image.resize((self.root.winfo_width(), self.root.winfo_height()))
            self.tk_image = ImageTk.PhotoImage(image)
            self.background_label.config(image=self.tk_image)
            self.background_label.image = self.tk_image
        except Exception as e:
            print(f"Ошибка: {e}")
    


if __name__ == "__main__":
    root = tk.Tk()
    root.config(bg='black', bd=3, relief='ridge')
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    root.wm_attributes('-alpha', 0.9)
    root.resizable(0, 0)
    root.geometry('540x420')
    app = DelayedApp(root)
    root.mainloop()
