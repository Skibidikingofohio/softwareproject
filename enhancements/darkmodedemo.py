import tkinter as tk
from tkinter import ttk

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard Dark Mode Demo")
        self.root.geometry("400x300")
        self.dark_mode = False

        self.setup_styles()
        self.setup_widgets()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure('Light.TProgressbar',
                             troughcolor='white',
                             background='green')
        self.style.configure('Dark.TProgressbar',
                             troughcolor='#333',
                             background='lime')

    def setup_widgets(self):
        self.root.configure(bg='white')

        self.card_label = tk.Label(
            self.root,
            text='你好 (nǐ hǎo) = Hello',
            font=('Arial', 20),
            bg='white',
            fg='black'
        )
        self.card_label.pack(pady=20)

        self.progress_bar = ttk.Progressbar(
            self.root,
            style='Light.TProgressbar',
            orient='horizontal',
            length=250,
            mode='determinate'
        )
        self.progress_bar['value'] = 34  # Simulate progress %
        self.progress_bar.pack(pady=10)

        self.toggle_btn = tk.Button(
            self.root,
            text='Dark Mode',
            command=self.toggle_theme
        )
        self.toggle_btn.pack()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        bg = '#111' if self.dark_mode else '#fff'
        fg = '#fff' if self.dark_mode else '#000'

        self.root.configure(bg=bg)
        self.card_label.configure(bg=bg, fg=fg)
        self.progress_bar.configure(style='Dark.TProgressbar' if self.dark_mode else 'Light.TProgressbar')
        self.toggle_btn.configure(text='Light Mode' if self.dark_mode else 'Dark Mode')


if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
