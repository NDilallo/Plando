import tkinter as tk
from tkinter import messagebox, filedialog

def submit_data(root):
    # Check for "None Selected" values
    if "None Selected" in ([dropdown.get() for dropdown in user_selections.values()] + [dropdown.get() for dropdown in user_boss_selections.values()]):
        messagebox.showerror("Error", "Please make a selection for all entries!")
    else:
        # Create a dictionary with user selections
        dungeon_selections = {
            text: dropdown.get() for text, dropdown in user_selections.items()
        }
        boss_selections = {
            text: dropdown.get() for text, dropdown in user_boss_selections.items()
        }
        # Check for duplicate values
        unique_dungeon_values = set(dungeon_selections.values())
        unique_boss_values = set(boss_selections.values())
        if len(unique_dungeon_values) != len(dungeon_selections) or len(unique_boss_values) != len(boss_selections):
            messagebox.showerror(
                "Error", "Please select unique values for all entries!"
            )
        else:
            try:
                print(dungeon_selections)
                print(boss_selections)
                CreateSeed.create_seed(dungeon_selections)
                CreateSeed.create_seed_bosses(boss_selections)
                messagebox.showinfo("Success", "Seed created successfully!")
            except:
                messagebox.showerror(
                    "Error", "Something went wrong when creating the file"
                )
