import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import random
import traceback

# Import with error handling
try:
    from speak import speak
except ImportError:
    def speak(text):
        print(f"🔊 Would speak: {text}")
        print("TTS module not available")

try:
    from quiz import run_quiz
except ImportError:
    def run_quiz(app, card, callback):
        print("Quiz module not available")
        callback(card['meaning'], card)

class FlashcardApp:
    def __init__(self, root, cards, stats, save_stats, save_cards):
        self.root = root
        self.root.title("🀄 Mandarin Flashcards")
        self.root.configure(bg='#f0f8ff')
        self.root.geometry("600x700")
        
        # Data
        self.cards = cards if cards else []
        self.stats = stats if stats else {"correct": 0, "total": 0, "learned": [], "per_category": {}}
        self.save_stats = save_stats
        self.save_cards = save_cards
        
        # State
        self.categories = sorted(set(card['category'] for card in self.cards)) if self.cards else []
        self.current_category = tk.StringVar(value="All")
        self.current = None
        self.front_visible = True
        
        # Create UI
        self._create_ui()
        
        # Initialize
        if not self.cards:
            self._show_no_cards_message()
        else:
            self.load_next()
    
    def _create_ui(self):
        """Create the user interface"""
        # Main title
        title_label = tk.Label(
            self.root,
            text="🀄 Mandarin Flashcards",
            font=("Helvetica", 24, 'bold'),
            bg='#f0f8ff',
            fg='#2c3e50'
        )
        title_label.pack(pady=15)
        
        # Category selection
        category_frame = tk.Frame(self.root, bg='#f0f8ff')
        category_frame.pack(pady=10)
        
        tk.Label(
            category_frame,
            text="Category:",
            font=("Helvetica", 12),
            bg='#f0f8ff',
            fg='#555'
        ).pack(side='left', padx=5)
        
        if self.categories:
            category_menu = ttk.Combobox(
                category_frame,
                textvariable=self.current_category,
                values=["All"] + self.categories,
                state="readonly",
                font=("Helvetica", 11)
            )
            category_menu.pack(side='left', padx=5)
            category_menu.bind('<<ComboboxSelected>>', self._on_category_change)
        
        # Flashcard display
        self.card_frame = tk.Frame(self.root, bg='#f0f8ff')
        self.card_frame.pack(pady=20)
        
        self.card_canvas = tk.Canvas(
            self.card_frame,
            width=400,
            height=200,
            bg='#ffffff',
            highlightthickness=3,
            highlightbackground='#3498db',
            relief='raised',
            bd=2
        )
        self.card_canvas.pack()
        
        self.card_text = self.card_canvas.create_text(
            200, 100,
            text="Click Next to start!",
            font=("Helvetica", 20, "bold"),
            fill="#2c3e50",
            width=380,
            justify='center'
        )
        
        # Control buttons
        self._create_control_buttons()
        
        # Quiz section
        self._create_quiz_section()
        
        # Stats section
        self._create_stats_section()
    
    def _create_control_buttons(self):
        """Create control buttons"""
        button_frame = tk.Frame(self.root, bg='#f0f8ff')
        button_frame.pack(pady=15)
        
        button_style = {
            'font': ("Helvetica", 12, "bold"),
            'bg': "#3498db",
            'fg': "white",
            'activebackground': "#2980b9",
            'relief': 'raised',
            'bd': 2,
            'padx': 15,
            'pady': 8,
            'cursor': 'hand2'
        }
        
        self.flip_btn = tk.Button(
            button_frame,
            text="🔄 Flip Card",
            command=self._safe_flip_card,
            **button_style
        )
        self.flip_btn.pack(side='left', padx=5)
        
        next_style = button_style.copy()
        next_style['bg'] = "#27ae60"
        next_style['activebackground'] = "#229954"
        
        self.next_btn = tk.Button(
            button_frame,
            text="➡️ Next Card",
            command=self._safe_load_next,
            **next_style
        )
        self.next_btn.pack(side='left', padx=5)
        
        speak_style = button_style.copy()
        speak_style['bg'] = "#e74c3c"
        speak_style['activebackground'] = "#c0392b"
        
        self.speak_btn = tk.Button(
            button_frame,
            text="🔊 Speak",
            command=self._safe_speak,
            **speak_style
        )
        self.speak_btn.pack(side='left', padx=5)
    
    def _create_quiz_section(self):
        """Create quiz section"""
        quiz_frame = tk.Frame(self.root, bg='#f0f8ff')
        quiz_frame.pack(pady=20, padx=20, fill='x')
        
        # Quiz title
        quiz_title = tk.Label(
            quiz_frame,
            text="📝 Quiz Time!",
            font=("Helvetica", 16, "bold"),
            bg='#f0f8ff',
            fg='#8e44ad'
        )
        quiz_title.pack(pady=10)
        
        # Question label
        self.question = tk.Label(
            quiz_frame,
            text="Select the correct meaning:",
            font=("Helvetica", 13),
            bg='#f0f8ff',
            fg='#2c3e50',
            wraplength=500
        )
        self.question.pack(pady=10)
        
        # Choices frame
        self.choices_frame = tk.Frame(quiz_frame, bg='#f0f8ff')
        self.choices_frame.pack(pady=10, fill='x')
    
    def _create_stats_section(self):
        """Create stats section"""
        stats_frame = tk.Frame(self.root, bg='#ecf0f1', relief='sunken', bd=2)
        stats_frame.pack(pady=20, padx=20, fill='x')
        
        stats_title = tk.Label(
            stats_frame,
            text="📊 Your Progress",
            font=("Helvetica", 14, "bold"),
            bg='#ecf0f1',
            fg='#34495e'
        )
        stats_title.pack(pady=10)
        
        self.stats_label = tk.Label(
            stats_frame,
            text="Ready to start learning! 🚀",
            font=("Helvetica", 12),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        self.stats_label.pack(pady=10)
    
    def _show_no_cards_message(self):
        """Show message when no cards are available"""
        self.card_canvas.itemconfig(
            self.card_text,
            text="⚠️ No flashcards found!\n\nPlease check your flashcards.json file.",
            font=("Helvetica", 14),
            fill="#e74c3c"
        )
        
        # Disable buttons
        for btn in [self.flip_btn, self.next_btn, self.speak_btn]:
            btn.config(state="disabled")
        
        self.stats_label.config(text="No cards available to study.")
    
    def _on_category_change(self, event=None):
        """Handle category change"""
        try:
            self.load_next()
        except Exception as e:
            print(f"Category change error: {e}")
    
    def _safe_flip_card(self):
        """Safely flip card with error handling"""
        try:
            self.flip_card()
        except Exception as e:
            print(f"Flip card error: {e}")
            messagebox.showerror("Error", "Failed to flip card")
    
    def _safe_load_next(self):
        """Safely load next card with error handling"""
        try:
            self.load_next()
        except Exception as e:
            print(f"Load next error: {e}")
            messagebox.showerror("Error", "Failed to load next card")
    
    def _safe_speak(self):
        """Safely speak word with error handling"""
        try:
            self.speak_word()
        except Exception as e:
            print(f"Speak error: {e}")
            messagebox.showwarning("TTS Error", "Text-to-speech not available")
    
    def load_next(self):
        """Load next flashcard"""
        if not self.cards:
            return
        
        # Get cards for current category
        if self.current_category.get() == "All":
            pool = self.cards
        else:
            pool = [c for c in self.cards if c['category'] == self.current_category.get()]
        
        if not pool:
            self.card_canvas.itemconfig(
                self.card_text,
                text="⚠️ No cards in this category",
                font=("Helvetica", 14),
                fill="#e74c3c"
            )
            return
        
        # Select random card (prioritize due cards)
        now = datetime.now()
        due_cards = []
        
        for card in pool:
            try:
                next_review = datetime.fromisoformat(card.get("next_review", "1970-01-01T00:00:00"))
                if next_review <= now:
                    due_cards.append(card)
            except ValueError:
                due_cards.append(card)  # Include cards with invalid dates
        
        self.current = random.choice(due_cards if due_cards else pool)
        self.front_visible = True
        self.update_card()
        self.run_quiz()
        self.update_stats_display()
    
    def update_card(self):
        """Update card display"""
        if not self.current:
            return
        
        if self.front_visible:
            text = self.current["word"]
            font = ("Helvetica", 28, "bold")
            color = "#2c3e50"
        else:
            text = f'{self.current["meaning"]}\n({self.current["pinyin"]})'
            font = ("Helvetica", 18)
            color = "#27ae60"
        
        self.card_canvas.itemconfig(
            self.card_text,
            text=text,
            font=font,
            fill=color
        )
    
    def flip_card(self):
        """Flip the flashcard"""
        if not self.current:
            return
        
        self.front_visible = not self.front_visible
        self.update_card()
    
    def speak_word(self):
        """Speak the current word"""
        if not self.current:
            return
        
        try:
            speak(self.current['word'])
        except Exception as e:
            print(f"Speech error: {e}")
    
    def run_quiz(self):
        """Run quiz for current card"""
        if not self.current:
            return
        
        try:
            run_quiz(self, self.current, self.check_answer)
        except Exception as e:
            print(f"Quiz error: {e}")
            # Fallback: show simple continue button
            for widget in self.choices_frame.winfo_children():
                widget.destroy()
            
            fallback_btn = tk.Button(
                self.choices_frame,
                text="Continue (Quiz Error)",
                command=lambda: self.check_answer(self.current['meaning'], self.current),
                font=("Helvetica", 12),
                bg="#f39c12",
                fg="white"
            )
            fallback_btn.pack(pady=10)
    
    def check_answer(self, choice, card):
        """Check quiz answer and update stats"""
        try:
            is_correct = choice == card['meaning']
            category = card['category']
            
            # Update stats
            self.stats['total'] += 1
            if category not in self.stats['per_category']:
                self.stats['per_category'][category] = {"correct": 0, "total": 0}
            
            self.stats['per_category'][category]['total'] += 1
            
            if is_correct:
                self.stats['correct'] += 1
                self.stats['per_category'][category]['correct'] += 1
                
                # Add to learned words
                if card['word'] not in self.stats['learned']:
                    self.stats['learned'].append(card['word'])
                
                # Speak correct answer
                try:
                    speak(card['word'])
                except:
                    pass
            
            # Update spaced repetition
            ease = card.get("ease", 2)
            ease = min(ease + 1, 5) if is_correct else max(ease - 1, 1)
            days = ease ** 2
            
            card['ease'] = ease
            card['next_review'] = (datetime.now() + timedelta(days=days)).isoformat()
            
            # Save data
            self.save_stats()
            self.save_cards()
            
            # Load next card after short delay
            self.root.after(1000, self.load_next)
            
        except Exception as e:
            print(f"Answer check error: {e}")
            traceback.print_exc()
    
    def update_stats_display(self):
        """Update stats display"""
        try:
            category = self.current_category.get()
            
            if category == "All":
                total_correct = self.stats['correct']
                total_attempts = self.stats['total']
                percentage = (total_correct / total_attempts * 100) if total_attempts > 0 else 0
                
                text = f"Overall: {total_correct}/{total_attempts} correct ({percentage:.1f}%)"
                if self.stats['learned']:
                    text += f"\nWords learned: {len(self.stats['learned'])}"
            else:
                cat_stats = self.stats['per_category'].get(category, {"correct": 0, "total": 0})
                correct = cat_stats['correct']
                total = cat_stats['total']
                percentage = (correct / total * 100) if total > 0 else 0
                
                text = f"{category}: {correct}/{total} correct ({percentage:.1f}%)"
            
            self.stats_label.config(text=text)
            
        except Exception as e:
            print(f"Stats update error: {e}")
            self.stats_label.config(text="Stats unavailable")