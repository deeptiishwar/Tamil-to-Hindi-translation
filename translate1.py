import tkinter as tk
from tkinter import messagebox
import spacy

# Load English language model from spaCy
nlp = spacy.load("en_core_web_sm")

def load_dataset(file_path):
    hindi_to_tamil = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split("\\t")  # Try splitting using '\t'
            if len(parts) == 1:
                parts = line.strip().split('|')  # Try splitting using '|'
            if len(parts) != 2:
                continue 
            hindi,tamil = parts
            hindi_to_tamil[hindi.strip()] = tamil.strip()
    return hindi_to_tamil

def translate_to_tamil(hindi_word, hindi_to_tamil):
    tamil_words = []
    if hindi_word in hindi_to_tamil:
        return hindi_to_tamil[hindi_word]
    for h in hindi_word.split(' '):
        if h in hindi_to_tamil:
            tamil_translation = hindi_to_tamil.get(h)
        else:
            tamil_translation1=[]
            for u in h:
                tamil_translation1.append(hindi_to_tamil[u])
            tamil_translation=''.join(tamil_translation1)
        tamil_words.append(tamil_translation)
    return ' '.join(tamil_words)

def nlp_analysis(text):
    doc = nlp(text)
    analysis = {
        "tokens": [],
        "entities": [],
        "sentiment": doc.sentiment
    }
    for token in doc:
        analysis["tokens"].append((token.text, token.lemma_, token.pos_, token.tag_))
    for ent in doc.ents:
        analysis["entities"].append((ent.text, ent.label_))
    return analysis

def translate_word():
    hindi_word = hindi_entry.get().strip()
    if not hindi_word:
        messagebox.showwarning("Warning", "Please enter a Hindi word.")
        return
    tamil_translation = translate_to_tamil(hindi_word, hindi_to_tamil_dict)
    nlp_result = nlp_analysis(hindi_word)
    print(nlp_result['tokens'])
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, f"You: {hindi_word}\n", "user")
    chat_history.insert(tk.END, f"Computer (Translation): {tamil_translation}\n", "computer")
    chat_history.insert(tk.END, "NLP Analysis:\n", "analysis_title")
    chat_history.insert(tk.END, f"Sentiment Score: {nlp_result['sentiment']}\n", "analysis")
    chat_history.config(state=tk.DISABLED)


# Load dataset
dataset_file_path = '/Users/deeptiishwar/Desktop/NNlp/main/nlp.txt'
hindi_to_tamil_dict = load_dataset(dataset_file_path)

# Create GUI window
window = tk.Tk()
window.title("Hindi to Tamil Translator")
window.configure(bg="teal")

# Create widgets
label = tk.Label(window, text="Enter a Hindi word:")
hindi_entry = tk.Entry(window, width=50)
translate_button = tk.Button(window, text="Translate", command=translate_word)
chat_history = tk.Text(window, height=20, width=50,background="black")
chat_history.config(state=tk.DISABLED)

# Apply styles
chat_history.tag_configure("user", foreground="blue", justify="right")
chat_history.tag_configure("computer", foreground="white", justify="left")
chat_history.tag_configure("analysis_title", foreground="black", justify="left", font=("Arial", 10, "bold"))
chat_history.tag_configure("analysis", foreground="black", justify="left")

# Place widgets
label.grid(row=0, column=0, padx=10, pady=10)
hindi_entry.grid(row=0, column=1, padx=10, pady=10)
translate_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
chat_history.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Run the application
window.mainloop()
