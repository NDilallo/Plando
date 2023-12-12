import tkinter as tk
from tkinter import messagebox, filedialog
import CreateSeed
import shutil
import os
from enum import Enum
import SubmitInputs
import UpdateSeed

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
# user_boss_selections = {}


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
    # if selection_type == SelectionType.DUNGEON:
    user_selections[text] = dropdown
    # elif selection_type == SelectionType.BOSS:
    #     user_boss_selections[text] = dropdown


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
        # boss_selections = {
        #     text: dropdown.get() for text, dropdown in user_boss_selections.items()
        # }
        # Check for duplicate values
        unique_dungeon_values = set(dungeon_selections.values())
        # unique_boss_values = set(boss_selections.values())
        if len(unique_dungeon_values) != len(dungeon_selections):
            messagebox.showerror(
                "Error", "Please select unique values for all entries!"
            )
        else:
            try:
                print(dungeon_selections)
                translated_index_pairs = SubmitInputs.submit_inputs(dungeon_selections)
                print("Past")
                index_pairs.extend(translated_index_pairs)
                print(f"index_pairs: {index_pairs}")
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

# Title label - Dungeon Entrances
title_label = tk.Label(
    root, text="Dungeon Entrances", font=("Arial", 14, "bold"), bg="lightgray"
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
for text in texts_dungeon:
    create_row(root, text, SelectionType.DUNGEON)

# Add space between sections
spacer_label = tk.Label(root, text="")  # Empty label for space
spacer_label.pack()

# Create multiple rows - Boss Entrances
for text in texts_dungeon:
    if text in ["Ice Cavern", "Bottom of the Well", "Gerudo Training Grounds"]:
        continue
    text = text + " Boss"
    create_row(root, text, SelectionType.BOSS)


# Add space between sections
spacer_label = tk.Label(root, text="")  # Empty label for space
spacer_label.pack()


# File upload button
upload_button = tk.Button(
    root, text="Upload File", command=upload_file, bg="orange", fg="white"
)
upload_button.pack(pady=10)

# Add space between sections
spacer_label = tk.Label(root, text="", bg="lightgray")
spacer_label.pack()

# Submit button
submit_button = tk.Button(
    root, text="Submit", command=submit_data, bg="skyblue", fg="white"
)
submit_button.pack(pady=10)


root.mainloop()
