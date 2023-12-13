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

curr_text_input_row = 0
curr_row = 0

index_pairs = list()

class SelectionType(Enum):
    DUNGEON = dungeon_options
    BOSS = boss_options
    SONG = 3
    OWL = 4

# Dictionary to store user selections
user_selections = {}
user_song_selections = {}
custom_swap_selections = ()


def create_row(root, text, selection_type, texts_dungeon):
    global curr_row
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=5)

    label = tk.Label(frame, text=f"{text}:", width=len(max(texts_dungeon, key=len)), anchor="e")  # Align text to the right
    label.grid(row=curr_row, column=0, sticky='e')  # Sticky parameter to align to the east (right)

    dropdown = tk.StringVar(root)
    dropdown.set("None Selected")
    dropdown_menu = tk.OptionMenu(frame, dropdown, *selection_type.value)
    dropdown_menu.grid(row=curr_row, column=1)

    curr_row += 1

    # Store user selections
    user_selections[text] = dropdown


def create_text_input_row(root, text, texts):
    global curr_text_input_row
    frame = tk.Frame(root, bg="white")
    frame.pack(padx=10, pady=5)
    
    label = tk.Label(frame, text=f"{text}:", width=len(max(texts, key=len)), anchor="w")
    # label.pack(side="left")
    label.grid(row=curr_text_input_row, column=0)
    
    entry = tk.Entry(frame)
    # entry.pack(side="left", padx=5)
    entry.grid(row=curr_text_input_row, column=1)

    curr_text_input_row += 1

    user_song_selections[text] = entry

def create_index_swap(root):
    global custom_swap_selections  # Declare as global

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=5)

    label = tk.Label(frame, text="Entrance: ", anchor="w")
    label.grid(row=0, column=0, sticky="ns")

    entrance1 = tk.Entry(frame)
    entrance1.grid(row=0, column=1, padx=5, sticky="ns")

    label = tk.Label(frame, text="--->", anchor="w")
    label.grid(row=0, column=2, sticky="ns")

    entrance2 = tk.Entry(frame)
    entrance2.grid(row=0, column=3, padx=5, sticky="ns")

    label = tk.Label(frame, text="Exit: ", anchor="w")
    label.grid(row=1, column=0, sticky="ns")

    exit1 = tk.Entry(frame)
    exit1.grid(row=1, column=1, padx=5, sticky="ns")

    exit2 = tk.Entry(frame)
    exit2.grid(row=1, column=3, padx=5, sticky="ns")

    # Adjusting row weights to center vertically
    frame.grid_rowconfigure(0, weight=1)

    custom_swap_selections = (entrance1, exit1, entrance2, exit2)
    
    enter_swap_button = tk.Button(
    second_frame, text="Swap", command=swap_indexes, bg="skyblue", fg="white")
    enter_swap_button.pack(pady=10)


def upload_file():
    file_path = filedialog.askopenfilename()  # Open file dialog to select a file
    # Check if a file is selected
    if file_path:
        # Copy the selected file to a certain directory (e.g., 'destination_folder')
        destination_folder = os.getcwd()  # Replace with your desired directory
        shutil.copy(file_path, destination_folder)
        messagebox.showinfo("Success", f"File {file_path} uploaded successfully")

def swap_indexes():
    global custom_swap_selections
    if custom_swap_selections[0].get() == "" or custom_swap_selections[1].get() == "":
        messagebox.showerror("Error", "Please Enter a Hex Value into both Boxes")
    elif not custom_swap_selections[0].get().isalnum() or not custom_swap_selections[1].get().isalnum():
        messagebox.showerror("Error", "Indexes should be alphanumeric, no special symbols! - Hex entries")
    else:
        index_pairs.append((int(custom_swap_selections[0].get(), 16), int(custom_swap_selections[1].get(), 16), int(custom_swap_selections[2].get(), 16), int(custom_swap_selections[3].get(), 16)))
        custom_swap_selections[0].delete(0, tk.END)
        custom_swap_selections[1].delete(0, tk.END)
        custom_swap_selections[2].delete(0, tk.END)
        custom_swap_selections[3].delete(0, tk.END)

def submit_data():
    # Check for "None Selected" values
    if "None Selected" in [dropdown.get() for dropdown in user_selections.values()] or None in [entry.get() for entry in user_song_selections.values()]:
        messagebox.showerror("Error", "Please make a selection for all entries!")
    else:
        # Create a dictionary with user selections
        dungeon_selections = {
            text: dropdown.get() for text, dropdown in user_selections.items()
        }

        warp_song_selections = {}
        for text, entry in user_song_selections.items():
            if not entry.get().isalnum():
                messagebox.showerror("Error", "Indexes should be alphanumeric, no special symbols! - Hex entries")
                break  # Stop processing further if there's an error
            else:
                warp_song_selections[text] = entry.get()

        # Check for duplicate values
        unique_dungeon_values = set(dungeon_selections.values())
        # unique_boss_values = set(boss_selections.values())
        if len(unique_dungeon_values) != len(dungeon_selections):
            messagebox.showerror(
                "Error", "Please select unique values for all entries!"
            )
        else:
            try:
                translated_index_pairs = SubmitInputs.submit_inputs_dungeons_bosses(dungeon_selections)
                index_pairs.extend(translated_index_pairs)
                translated_index_pairs = SubmitInputs.submit_inputs_warp_songs(warp_song_selections)
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
    create_row(second_frame, text, SelectionType.DUNGEON, texts_dungeon)

# Add space between sections
spacer_label = tk.Label(second_frame, text="")  # Empty label for space
spacer_label.pack()

# Title label - Boss Entrances
title_label = tk.Label(
    second_frame, text="Boss Entrances", font=("Arial", 14, "bold"), bg="lightgray"
)
title_label.pack()

# Create multiple rows - Boss Entrances
for text in texts_dungeon:
    if text in ["Ice Cavern", "Bottom of the Well", "Gerudo Training Grounds"]:
        continue
    text = text + " Boss"
    create_row(second_frame, text, SelectionType.BOSS, texts_dungeon)


# Add space between sections
spacer_label = tk.Label(second_frame, text="")  # Empty label for space
spacer_label.pack()

# Title label - Warp Songs
title_label = tk.Label(
    second_frame, text="Warp Songs", font=("Arial", 14, "bold"), bg="lightgray"
)
title_label.pack()
# Subtext label - Warp Songs
title_label = tk.Label(
    second_frame, text="Enter Destination's Hex Value", font=("Arial", 8, "bold"), bg="lightgray"
)
title_label.pack()

# Create multiple rows - Warp Songs
for text in texts_warp_songs:
    create_text_input_row(second_frame, text, texts_warp_songs)

# Add space between sections
spacer_label = tk.Label(second_frame, text="")  # Empty label for space
spacer_label.pack()

# Title label - Custom Index Swaps
title_label = tk.Label(
    second_frame, text="Index Swap", font=("Arial", 14, "bold"), bg="lightgray"
)
title_label.pack()
# Subtext label - Custom Index Swaps
title_label = tk.Label(
    second_frame, text="Optional: Swap any entrance (left) with any other (or same) entrance (right)\nNOTE: You must have overworld entrance randomizer enabled for this to work!", font=("Arial", 8, "bold"), bg="lightgray"
)
title_label.pack()

# Create index swap section
create_index_swap(second_frame)

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
    second_frame, text="Submit", command=submit_data, bg="green", fg="white"
)
submit_button.pack(pady=10)


root.mainloop()