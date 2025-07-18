import random
import tkinter as tk
from tkinter import ttk

def run_quiz(app, card, callback):
    """
    Generate a multiple choice quiz for a flashcard
    Robust error handling for offline use
    """
    try:
        # Clear previous widgets
        for widget in app.choices_frame.winfo_children():
            widget.destroy()
        
        # Set question with better formatting
        question_text = f"What does '{card['word']}' ({card['pinyin']}) mean?"
        app.question.config(text=question_text)
        
        # Get correct answer
        correct_answer = card['meaning']
        
        # Check if we have enough cards for multiple choice
        available_cards = [c for c in app.cards if c['meaning'] != correct_answer]
        
        if len(available_cards) < 2:
            # Not enough cards for multiple choice - show direct answer
            _show_direct_answer(app, card, callback)
            return
        
        # Generate wrong answers
        wrong_answers = []
        attempts = 0
        max_attempts = 50  # Prevent infinite loops
        
        while len(wrong_answers) < 3 and attempts < max_attempts:
            random_card = random.choice(available_cards)
            if random_card['meaning'] not in wrong_answers:
                wrong_answers.append(random_card['meaning'])
            attempts += 1
        
        # Create options list
        options = [correct_answer] + wrong_answers
        random.shuffle(options)
        
        # Create choice buttons with better styling
        button_style = {
            'font': ('Helvetica', 11),
            'bg': '#e3f2fd',
            'fg': '#1976d2',
            'activebackground': '#bbdefb',
            'relief': 'raised',
            'bd': 2,
            'padx': 10,
            'pady': 8,
            'cursor': 'hand2'
        }
        
        # Create buttons in a grid for better layout
        for i, option in enumerate(options):
            row = i // 2
            col = i % 2
            
            btn = tk.Button(
                app.choices_frame,
                text=option,
                command=lambda opt=option: _handle_answer(app, opt, card, callback),
                wraplength=200,  # Wrap long text
                justify='center',
                **button_style
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
        
        # Configure grid weights for responsive layout
        app.choices_frame.grid_columnconfigure(0, weight=1)
        app.choices_frame.grid_columnconfigure(1, weight=1)
        
        # Add a "Show Answer" button for learning
        show_answer_btn = tk.Button(
            app.choices_frame,
            text="💡 Show Answer",
            command=lambda: _show_correct_answer(app, correct_answer),
            font=('Helvetica', 10),
            bg='#fff3e0',
            fg='#f57c00',
            relief='raised',
            bd=2,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        show_answer_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
    except Exception as e:
        print(f"Quiz generation error: {e}")
        _show_error_fallback(app, card, callback)

def _show_direct_answer(app, card, callback):
    """Show answer directly when not enough cards for multiple choice"""
    # Create info label
    info_label = tk.Label(
        app.choices_frame,
        text=f"'{card['word']}' ({card['pinyin']}) means:",
        font=('Helvetica', 12),
        bg='#f0f0f0',
        fg='#555'
    )
    info_label.pack(pady=10)
    
    # Create answer display
    answer_frame = tk.Frame(app.choices_frame, bg='#e8f5e8', relief='raised', bd=2)
    answer_frame.pack(pady=10, padx=20, fill='x')
    
    answer_label = tk.Label(
        answer_frame,
        text=card['meaning'],
        font=('Helvetica', 14, 'bold'),
        bg='#e8f5e8',
        fg='#2e7d32',
        pady=15
    )
    answer_label.pack()
    
    # Continue button
    continue_btn = tk.Button(
        app.choices_frame,
        text="✅ Continue",
        command=lambda: callback(card['meaning'], card),
        font=('Helvetica', 12),
        bg='#4caf50',
        fg='white',
        relief='raised',
        bd=2,
        padx=20,
        pady=8,
        cursor='hand2'
    )
    continue_btn.pack(pady=10)

def _handle_answer(app, selected_option, card, callback):
    """Handle quiz answer selection"""
    try:
        # Disable all buttons to prevent multiple clicks
        for widget in app.choices_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state='disabled')
        
        # Visual feedback
        correct_answer = card['meaning']
        is_correct = selected_option == correct_answer
        
        # Update button colors
        for widget in app.choices_frame.winfo_children():
            if isinstance(widget, tk.Button) and widget.cget('text') in [selected_option, correct_answer]:
                if widget.cget('text') == correct_answer:
                    widget.config(bg='#4caf50', fg='white')  # Green for correct
                elif widget.cget('text') == selected_option and not is_correct:
                    widget.config(bg='#f44336', fg='white')  # Red for wrong selection
        
        # Small delay before proceeding
        app.root.after(1500, lambda: callback(selected_option, card))
        
    except Exception as e:
        print(f"Answer handling error: {e}")
        callback(selected_option, card)

def _show_correct_answer(app, correct_answer):
    """Highlight the correct answer"""
    for widget in app.choices_frame.winfo_children():
        if isinstance(widget, tk.Button) and widget.cget('text') == correct_answer:
            widget.config(bg='#4caf50', fg='white')
            widget.config(text=f"✅ {correct_answer}")
            break

def _show_error_fallback(app, card, callback):
    """Show error message and continue button"""
    error_label = tk.Label(
        app.choices_frame,
        text=f"Quiz Error!\n{card['word']} ({card['pinyin']}) = {card['meaning']}",
        font=('Helvetica', 12),
        bg='#ffebee',
        fg='#d32f2f',
        pady=20,
        wraplength=300
    )
    error_label.pack(pady=20)
    
    continue_btn = tk.Button(
        app.choices_frame,
        text="Continue",
        command=lambda: callback(card['meaning'], card),
        font=('Helvetica', 12),
        bg='#f44336',
        fg='white',
        padx=20,
        pady=8
    )
    continue_btn.pack(pady=10)

