import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import random
from speak import speak
from quiz import run_quiz

class FlashcardApp:
    def __init__(self, root, cards, stats, save_stats, save_cards):
        self.root = root
        self.root.title("🀄 Mandarin Flashcards")
        self.root.configure(bg='#f0f0f0')
        self.cards, self.stats = cards, stats
        self.save_stats, self.save_cards = save_stats, save_cards

        self.categories = sorted(set(card['category'] for card in cards)) if cards else []
        self.current_category = tk.StringVar(value="All")
        self.current = None
        self.front_visible = True

        tk.Label(root, text="🀄 Mandarin Flashcards", font=("Helvetica",22,'bold'), bg='#f0f0f0', fg='#333').pack(pady=10)
        tk.Label(root, text="Filter by Category:", font=("Helvetica",12), bg='#f0f0f0', fg='#555').pack()
        if self.categories:
            tk.OptionMenu(root, self.current_category, "All", *self.categories, command=self.set_category).pack()

        self.card_canvas = tk.Canvas(root, width=350, height=180, bg='#ffffff', highlightthickness=2, highlightbackground='#ccc')
        self.card_text = self.card_canvas.create_text(175,90, text="", font=("Helvetica",28), fill="#222", width=320)
        self.card_canvas.pack(pady=20)

        btn_cfg = {"font":("Helvetica",14), "bg":"#4caf50", "fg":"white", "activebackground":"#388e3c", "bd":0, "padx":12, "pady":6}
        self.flip_btn = tk.Button(root, text="🔄 Flip", command=self.flip_card, **btn_cfg); self.flip_btn.pack(pady=5)
        self.next_btn = tk.Button(root, text="➡️ Next", command=self.load_next, **btn_cfg); self.next_btn.pack()
        self.speak_btn = tk.Button(root, text="🔊 Speak", command=self.speak_word, **btn_cfg); self.speak_btn.pack(pady=5)

        self.quiz_label = tk.Label(root, text="Quiz:", font=("Helvetica",16), bg="#f0f0f0", fg="#444"); self.quiz_label.pack(pady=10)
        self.question = tk.Label(root, text="", font=("Helvetica",14), bg="#f0f0f0"); self.question.pack()
        self.choices_frame = tk.Frame(root, bg="#f0f0f0"); self.choices_frame.pack()
        self.stats_label = tk.Label(root, text="", font=("Helvetica",12), bg="#f0f0f0"); self.stats_label.pack(pady=10)

        if not self.cards:
            messagebox.showerror("Error","No flashcards found!")
            self.card_canvas.create_text(175,90, text="⚠ No flashcards", font=("Helvetica",16), fill="red")
            self.flip_btn.config(state="disabled"); self.next_btn.config(state="disabled"); self.speak_btn.config(state="disabled")
        else:
            self.load_next()

    def set_category(self, _): self.load_next()

    def load_next(self):
        pool = self.cards if self.current_category.get()=="All" else [c for c in self.cards if c['category']==self.current_category.get()]
        if not pool:
            self.card_canvas.itemconfig(self.card_text,"⚠ No cards in this category."); return
        due = [c for c in pool if datetime.fromisoformat(c.get("next_review","1970-01-01"))<=datetime.now()]
        self.current = random.choice(due if due else pool)
        self.front_visible=True; self.update_card(); self.run_quiz(); self.update_stats_display()

    def update_card(self):
        txt = self.current["word"] if self.front_visible else f'{self.current["meaning"]} ({self.current["pinyin"]})'
        self.card_canvas.itemconfig(self.card_text, text=txt)

    def flip_card(self):
        self.front_visible = not self.front_visible
        self.update_card()

    def speak_word(self):
        speak(self.current['word'])

    def run_quiz(self):
        run_quiz(self, self.current, self.check_answer)

    def check_answer(self, choice):
        corr = choice==self.current['meaning']
        cat = self.current['category']
        self.stats['total'] += 1
        self.stats['per_category'].setdefault(cat, {"correct":0,"total":0})
        self.stats['per_category'][cat]['total'] += 1
        if corr:
            self.stats['correct'] += 1
            self.stats['per_category'][cat]['correct'] += 1
            speak(self.current['word'])
            if self.current['word'] not in self.stats['learned']:
                self.stats['learned'].append(self.current['word'])
        ease = self.current.get("ease",2)
        ease = min(ease+1,5) if corr else max(ease-1,1)
        days = ease**2
        self.current['ease'], self.current['next_review'] = ease, (datetime.now()+timedelta(days=days)).isoformat()
        self.save_stats(); self.save_cards(); self.load_next()

    def update_stats_display(self):
        cat = self.current_category.get()
        if cat=="All":
            txt = f"Total: {self.stats['correct']} / {self.stats['total']} correct"
        else:
            c,t = self.stats['per_category'].get(cat,{"correct":0,"total":0}).values()
            pct = (c/t*100) if t>0 else 0
            txt = f"{cat}: {c} / {t} correct ({pct:.0f}%)"
        self.stats_label.config(text=txt)
