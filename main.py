from typing import List
import tkinter as tk
import os


def filter_words(words: List[str], length: int = None, include_letters: str = None, exclude_letters: str = None, letters_at_positions: dict = None, starts_with: str = None, ends_with: str = None, first_letters: str = None) -> List[str]:
    """
    Filters a list of words based on the given criteria and returns the filtered list.
    """
    filtered_words = []
    for word in words:
        if length is not None and len(word) != length:
            continue
        if include_letters is not None and not all(letter in word for letter in include_letters):
            continue
        if exclude_letters is not None and any(letter in word for letter in exclude_letters):
            continue
        if letters_at_positions is not None:
            for position, letter in letters_at_positions.items():
                if len(word) <= position or word[position] != letter:
                    break
            else:
                filtered_words.append(word)
        elif starts_with is not None and not word.startswith(starts_with):
            continue
        elif ends_with is not None and not word.endswith(ends_with):
            continue
        elif first_letters is not None and not all(word[i] == letter for i, letter in enumerate(first_letters)):
            continue
        else:
            filtered_words.append(word)
    return filtered_words


def read_words_from_file(folder_path: str) -> List[str]:
    """
    Reads words from all text files in a folder and returns them as a sorted list without duplicates.
    """
    words = set()

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf8") as file:
                for word in file.read().split():
                    if word.isalpha():
                        words.add(word)
                
    return sorted(list(words))


def search():
    """
    Searches for words based on the given criteria and displays the results in the GUI.
    """
    length = int(length_entry.get()) if length_entry.get() else None
    include_letters = include_letters_entry.get() if include_letters_entry.get() else None
    exclude_letters = exclude_letters_entry.get() if exclude_letters_entry.get() else None
    starts_with = starts_with_entry.get() if starts_with_entry.get() else None
    ends_with = ends_with_entry.get() if ends_with_entry.get() else None
    first_letters = first_letters_entry.get() if first_letters_entry.get() else None
    letters_at_positions = {}
    if letters_at_positions_entry.get():
        for item in letters_at_positions_entry.get().split(','):
            position, letter = item.split(':')
            letters_at_positions[int(position)] = letter
    words = read_words_from_file("./paroleitaliane/")
    filtered_words = filter_words(words, length=length, include_letters=include_letters, exclude_letters=exclude_letters, letters_at_positions=letters_at_positions, starts_with=starts_with, ends_with=ends_with, first_letters=first_letters)
    results_text.delete("1.0", tk.END)
    results_text.insert(tk.END, f"Numero di risultati: {len(filtered_words)}\n")
    results_text.insert(tk.END, "\n".join(filtered_words))
    results_text.configure(state='disabled')


# Create the GUI
root = tk.Tk()
root.title("Cerca parole italiane")
root.geometry("500x500")

# Create the input fields
length_label = tk.Label(root, text="Lunghezza:")
length_label.pack()
length_entry = tk.Entry(root)
length_entry.pack()

include_letters_label = tk.Label(root, text="Lettere incluse:")
include_letters_label.pack()
include_letters_entry = tk.Entry(root)
include_letters_entry.pack()

exclude_letters_label = tk.Label(root, text="Lettere escluse:")
exclude_letters_label.pack()
exclude_letters_entry = tk.Entry(root)
exclude_letters_entry.pack()

starts_with_label = tk.Label(root, text="Inizia con:")
starts_with_label.pack()
starts_with_entry = tk.Entry(root)
starts_with_entry.pack()

ends_with_label = tk.Label(root, text="Finisce con:")
ends_with_label.pack()
ends_with_entry = tk.Entry(root)
ends_with_entry.pack()

first_letters_label = tk.Label(root, text="Prime lettere:")
first_letters_label.pack()
first_letters_entry = tk.Entry(root)
first_letters_entry.pack()

letters_at_positions_label = tk.Label(root, text="Lettere in posizione:")
letters_at_positions_label.pack()
letters_at_positions_entry = tk.Entry(root)
letters_at_positions_entry.pack()


# Create the search button
search_button = tk.Button(root, text="Cerca", command=search)
search_button.pack()

# Create the results field
results_label = tk.Label(root, text="Risultati:")
results_label.pack()
results_text = tk.Text(root)
results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(root, command=results_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
results_text.configure(yscrollcommand=scrollbar.set)

root.mainloop()
