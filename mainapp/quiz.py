# quiz.py

import random
import tkinter as tk

def run_quiz(app, card, callback):
    app.question.config(text=f"What does '{card['word']}' mean?")
    for widget in app.choices_frame.winfo_children():
        widget.destroy()

    correct = card['meaning']
    options = [correct]
    while len(options) < 3:
        r = random.choice(app.cards)['meaning']
        if r not in options:
            options.append(r)
    random.shuffle(options)

    for opt in options:
        btn = tk.Button(app.choices_frame, text=opt, command=lambda o=opt: callback(o, card))
        btn.pack(side='left', padx=5)
