import tkinter as tk, json, os, sys
from ui import FlashcardApp

def resource_path(rel):
    try: return os.path.join(sys._MEIPASS, rel)
    except: return os.path.join(os.path.abspath("."), rel)

CARDS_FILE = resource_path("mainapp/flashcards.json")
STATS_FILE = resource_path("mainapp/stats.json")

def load_json(path, default):
    if os.path.exists(path):
        try:
            return json.load(open(path, encoding='utf-8'))
        except:
            pass
    return default

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

cards = load_json(CARDS_FILE, [])
stats = load_json(STATS_FILE, {"correct":0,"total":0,"learned":[],"per_category":{}})

if __name__=="__main__":
    root = tk.Tk()
    FlashcardApp(root, cards, stats, lambda: save_json(STATS_FILE,stats), lambda: save_json(CARDS_FILE,cards))
    root.mainloop()



