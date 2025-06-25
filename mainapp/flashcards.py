import tkinter as tk
import json, random, os
from datetime import datetime, timedelta
import pyttsx3
from tkinter import messagebox
from quiz import run_quiz
import sys, os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

CARDS_FILE = resource_path("mainapp/flashcards.json")
STATS_FILE = resource_path("mainapp/stats.json")

def load_json(path, default):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return default
    return default

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

cards = load_json(CARDS_FILE, [])
stats = load_json(STATS_FILE, {
    "correct": 0,
    "total": 0,
    "learned": [],
    "per_category": {}
})

engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mandarin Flashcards")

        self.categories = sorted(set(card['category'] for card in cards)) if cards else []
        self.current_category = tk.StringVar(value="All")
        self.current = None
        self.front_visible = True
        self.cards = cards

        self.title = tk.Label(root, text="🀄 Mandarin Flashcards", font=("Arial", 20))
        self.title.pack(pady=10)

        tk.Label(root, text="Filter by Category:").pack()
        if self.categories:
            tk.OptionMenu(root, self.current_category, "All", *self.categories, command=self.set_category).pack()

        self.card = tk.Frame(root, width=300, height=150, relief='raised', borderwidth=2)
        self.card.pack(pady=10)
        self.card_text = tk.Label(self.card, text="", font=("Arial", 24), wraplength=280)
        self.card_text.pack(expand=True)

        self.flip_btn = tk.Button(root, text="🔄 Flip", command=self.flip_card)
        self.flip_btn.pack(pady=5)

        self.next_btn = tk.Button(root, text="➡️ Next", command=self.next_card)
        self.next_btn.pack()

        self.speak_btn = tk.Button(root, text="🔊 Speak", command=self.speak_word)
        self.speak_btn.pack(pady=5)

        self.quiz_label = tk.Label(root, text="Quiz:", font=("Arial", 16))
        self.quiz_label.pack(pady=10)

        self.question = tk.Label(root, text="", font=("Arial", 14))
        self.question.pack()

        self.choices_frame = tk.Frame(root)
        self.choices_frame.pack()

        self.stats_label = tk.Label(root, text="", font=("Arial", 12))
        self.stats_label.pack(pady=10)

        if not self.cards:
            messagebox.showerror("Error", "No flashcards found in the JSON file!")
            self.card_text.config(text="⚠ No flashcards loaded.")
            self.flip_btn.config(state="disabled")
            self.next_btn.config(state="disabled")
            self.speak_btn.config(state="disabled")
        else:
            self.load_next()

    def set_category(self, selected):
        self.load_next()

    def load_next(self):
        category = self.current_category.get()
        pool = self.cards if category == "All" else [c for c in self.cards if c['category'] == category]

        if not pool:
            self.card_text.config(text="⚠ No cards in this category.")
            return

        due = [c for c in pool if datetime.fromisoformat(c.get("next_review", "1970-01-01")) <= datetime.now()]
        self.current = random.choice(due if due else pool)
        self.front_visible = True
        self.update_card()
        self.run_quiz()
        self.update_stats_display()

    def update_card(self):
        if self.front_visible:
            self.card_text.config(text=self.current["word"])
        else:
            self.card_text.config(text=f'{self.current["meaning"]} ({self.current["pinyin"]})')

    def flip_card(self):
        self.front_visible = not self.front_visible
        self.update_card()

    def next_card(self):
        self.load_next()

    def speak_word(self):
        speak(self.current['word'])

    def run_quiz(self):
        run_quiz(self, self.current, self.check_answer)

    def check_answer(self, choice):
        correct = choice == self.current['meaning']
        category = self.current['category']

        stats['total'] += 1
        stats['per_category'].setdefault(category, {"correct": 0, "total": 0})
        stats['per_category'][category]['total'] += 1

        if correct:
            stats['correct'] += 1
            stats['per_category'][category]['correct'] += 1
            speak(self.current['word'])
            if self.current['word'] not in stats['learned']:
                stats['learned'].append(self.current['word'])

        ease = self.current.get("ease", 2)
        ease = min(ease + 1, 5) if correct else max(ease - 1, 1)
        days = ease ** 2
        self.current['ease'] = ease
        self.current['next_review'] = (datetime.now() + timedelta(days=days)).isoformat()

        save_json(STATS_FILE, stats)
        save_json(CARDS_FILE, cards)
        self.load_next()

    def update_stats_display(self):
        cat = self.current_category.get()
        if cat == "All":
            self.stats_label.config(text=f"Total: {stats['correct']} / {stats['total']} correct")
        else:
            cat_stats = stats['per_category'].get(cat, {"correct": 0, "total": 0})
            c, t = cat_stats['correct'], cat_stats['total']
            percent = (c / t * 100) if t > 0 else 0
            self.stats_label.config(text=f"{cat}: {c} / {t} correct ({percent:.0f}%)")

# RUN THE APP
if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()



