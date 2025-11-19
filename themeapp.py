# themes.py
class Themes:
    def __init__(self):
        self.themes = {
            "light": {
                "bg": "#FFFFFF",
                "fg": "#000000",
                "button_bg": "#F0F0F0",
                "button_fg": "#000000"
            },
            "dark": {
                "bg": "#222222",
                "fg": "#FFFFFF",
                "button_bg": "#333333",
                "button_fg": "#FFFFFF"
            }
        }
        self.current_theme = "light"

    def get_current_theme(self):
        return self.themes[self.current_theme]

    def set_theme(self, theme_name):
        if theme_name in self.themes:
            self.current_theme = theme_name
        else:
            raise ValueError("Неизвестная тема")

    def apply_theme(self, widget):
        theme = self.get_current_theme()
        config = widget.configure()
        
        # Применяем только поддерживаемые опции
        if 'background' in config:
            widget.configure(bg=theme["bg"])
        if 'foreground' in config:
            widget.configure(fg=theme["fg"])

    def apply_button_theme(self, button):
        theme = self.get_current_theme()
        button.configure(
            bg=theme["button_bg"],
            fg=theme["button_fg"]
        )
