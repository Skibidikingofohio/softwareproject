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
        
        # Debug: Print the card data to understand structure
        print(f"DEBUG: Card data = {card}")
        
        # Set question with better formatting
        question_text = f"What does '{card['word']}' ({card['pinyin']}) mean?"
        app.question.config(text=question_text)
        
        # Get correct answer
        correct_answer = card['meaning']
        print(f"DEBUG: Correct answer = '{correct_answer}'")
        
        # Check if we have enough cards for multiple choice
        available_cards = [c for c in app.cards if c['meaning'] != correct_answer]
        print(f"DEBUG: Available cards for wrong answers: {len(available_cards)}")
        
        if len(available_cards) < 3:
            # Not enough cards for multiple choice - show direct answer
            print("DEBUG: Not enough cards, showing direct answer")
            _show_direct_answer(app, card, callback)
            return
        
        # Generate wrong answers - improved logic
        wrong_answers = []
        shuffled_cards = available_cards.copy()
        random.shuffle(shuffled_cards)
        
        # Take first 3 unique meanings
        for wrong_card in shuffled_cards:
            if wrong_card['meaning'] not in wrong_answers and wrong_card['meaning'] != correct_answer:
                wrong_answers.append(wrong_card['meaning'])
                if len(wrong_answers) >= 3:
                    break
        
        print(f"DEBUG: Wrong answers = {wrong_answers}")
        
        # Fallback if we still don't have enough wrong answers
        if len(wrong_answers) < 3:
            print("DEBUG: Still not enough wrong answers, showing direct answer")
            _show_direct_answer(app, card, callback)
            return
        
        # Create options list with exactly 4 choices
        options = [correct_answer] + wrong_answers[:3]  # Ensure exactly 3 wrong answers
        random.shuffle(options)
        
        # Debug print
        print(f"Quiz for: {card['word']} ({card['pinyin']})")
        print(f"Correct answer: '{correct_answer}'")
        print(f"All options: {options}")
        print(f"Correct answer in options: {correct_answer in options}")
        
        # Verify correct answer is in options (safety check)
        if correct_answer not in options:
            print("ERROR: Correct answer not in options! Fixing...")
            options[0] = correct_answer
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
        
        # Create buttons in a 2x2 grid
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
        import traceback
        traceback.print_exc()
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
            if isinstance(widget, tk.Button) and "Show Answer" not in widget.cget('text'):
                widget.config(state='disabled')
        
        # Visual feedback
        correct_answer = card['meaning']
        is_correct = selected_option == correct_answer
        
        print(f"Selected: {selected_option}")
        print(f"Correct: {correct_answer}")
        print(f"Is correct: {is_correct}")
        
        # Update button colors
        for widget in app.choices_frame.winfo_children():
            if isinstance(widget, tk.Button) and "Show Answer" not in widget.cget('text'):
                button_text = widget.cget('text')
                if button_text == correct_answer:
                    widget.config(bg='#4caf50', fg='white')  # Green for correct
                elif button_text == selected_option and not is_correct:
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
            # Don't modify the text to avoid confusion
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
    