import tkinter as tk
from tkinter import Frame, messagebox, filedialog
import shutil
import os
from enum import Enum
import SubmitInputs
import UpdateSeed
from tkinter import *

dungeon_options = [
    "Deku Tree",
    "Dodongo's Cavern",
    "Jabu",
    "Forest",
    "Fire",
    "Ice Cavern",
    "Water",
    "Bottom of the Well",
    "Shadow",
    "Gerudo Training Grounds",
    "Spirit",
]

boss_options = [
    "Gohma",
    "King Dodongo",
    "Barinade",
    "Phantom Ganon",
    "Volvagia",
    "Morpha",
    "Bongo Bongo",
    "Twinrova"
]


index_pairs = list()

class SelectionType(Enum):
    DUNGEON = dungeon_options
    BOSS = boss_options
    SONG = 3
    OWL = 4

# Dictionary to store user selections
user_selections = {}


def create_row(root, text, selection_type):
    frame = tk.Frame(root, bg="white")  # Add a white background
    frame.pack(padx=10, pady=5, fill="x")  # Add padding

    label = tk.Label(frame, text=f"{text}:", width=15, anchor="w")
    label.pack(side="left")

    dropdown = tk.StringVar(root)
    dropdown.set("None Selected")
    dropdown_menu = tk.OptionMenu(frame, dropdown, *selection_type.value)
    dropdown_menu.pack(side="left", padx=5)

    # Store user selections
    user_selections[text] = dropdown

def create_text_input_row(root, text):
    frame = tk.Frame(root, bg="white")
    frame.pack(padx=10, pady=5, fill="x")
    
    label = tk.Label(frame, text=f"{text}:", width=15, anchor="w")
    label.pack(side="left")
    
    entry = tk.Entry(frame)
    entry.pack(side="left", padx=5)


def upload_file():
    file_path = filedialog.askopenfilename()  # Open file dialog to select a file
    # Check if a file is selected
    if file_path:
        # Copy the selected file to a certain directory (e.g., 'destination_folder')
        destination_folder = os.getcwd()  # Replace with your desired directory
        shutil.copy(file_path, destination_folder)
        messagebox.showinfo("Success", f"File {file_path} uploaded successfully")


def submit_data():
    # Check for "None Selected" values
    if "None Selected" in [dropdown.get() for dropdown in user_selections.values()]:
        messagebox.showerror("Error", "Please make a selection for all entries!")
    else:
        # Create a dictionary with user selections
        dungeon_selections = {
            text: dropdown.get() for text, dropdown in user_selections.items()
        }
        # Check for duplicate values
        unique_dungeon_values = set(dungeon_selections.values())
        # unique_boss_values = set(boss_selections.values())
        if len(unique_dungeon_values) != len(dungeon_selections):
            messagebox.showerror(
                "Error", "Please select unique values for all entries!"
            )
        else:
            try:
                translated_index_pairs = SubmitInputs.submit_inputs(dungeon_selections)
                index_pairs.extend(translated_index_pairs)
                UpdateSeed.updateSeed(index_pairs)
                messagebox.showinfo("Success", "Seed created successfully!")
            except:
                messagebox.showerror(
                    "Error", "Something went wrong when creating the file"
                )


# Create the main window
root = tk.Tk()
root.title("Plando Setup Locations")
root.configure(bg="lightgray")  # Set a light gray background

# Scrollbar stuff
main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)

my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

my_scrollbar = tk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

second_frame = Frame(my_canvas)

my_canvas.create_window((0,0), window=second_frame, anchor="nw")


# Title label - Dungeon Entrances
title_label = tk.Label(
    second_frame, text="Dungeon Entrances", font=("Arial", 14, "bold"), bg="lightgray"
)
title_label.pack()

# Create multiple rows - Dungeon Entrances
texts_dungeon = [
    "Deku Tree",
    "Dodongo's Cavern",
    "Jabu",
    "Forest",
    "Fire",
    "Ice Cavern",
    "Water",
    "Bottom of the Well",
    "Shadow",
    "Gerudo Training Grounds",
    "Spirit",
]
texts_warp_songs = [
    "Minuet of Forest",
    "Bolero of Fire",
    "Serenade of Water",
    "Nocturne of Shadow",
    "Requiem of Spirit",
    "Prelude of Light",
]

for text in texts_dungeon:
    create_row(second_frame, text, SelectionType.DUNGEON)

# Add space between sections
spacer_label = tk.Label(second_frame, text="")  # Empty label for space
spacer_label.pack()

# Create multiple rows - Boss Entrances
for text in texts_dungeon:
    if text in ["Ice Cavern", "Bottom of the Well", "Gerudo Training Grounds"]:
        continue
    text = text + " Boss"
    create_row(second_frame, text, SelectionType.BOSS)


# Add space between sections
spacer_label = tk.Label(second_frame, text="")  # Empty label for space
spacer_label.pack()

# Create multiple rows - Warp Songs
for text in texts_warp_songs:
    create_text_input_row(second_frame, text)

# Add space between sections
spacer_label = tk.Label(second_frame, text="")  # Empty label for space
spacer_label.pack()

# File upload button
upload_button = tk.Button(
    second_frame, text="Upload File", command=upload_file, bg="orange", fg="white"
)
upload_button.pack(pady=10)

# Add space between sections
spacer_label = tk.Label(second_frame, text="", bg="lightgray")
spacer_label.pack()

# Submit button
submit_button = tk.Button(
    second_frame, text="Submit", command=submit_data, bg="skyblue", fg="white"
)
submit_button.pack(pady=10)


root.mainloop()