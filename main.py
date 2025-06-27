import os
import json
import shutil
from customtkinter import *


def button_event():
    path = textbox.get().strip()
    if not path:
        insert_text("No path entered!\n")
        return
    if not os.path.isdir(path):
        insert_text("Invalid folder path!\n")
        return
    organizeFolder(path)


def selectfile():
    filename = filedialog.askdirectory()
    if filename:
        textbox.delete(0, END)
        textbox.insert(0, filename)
        organizeFolder(filename)


def insert_text(text):
    logger.configure(state="normal")
    logger.insert("end", text)
    logger.see("end")
    logger.configure(state="disabled")


def load_mapping():
    try:
        with open("file_map.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    

def save_mapping(mapping):
    with open("file_map.json", "w") as f:
        json.dump(mapping, f, indent=4)


def open_mapping_editor():
    editor = CTkToplevel(app)
    editor.title("Edit File Mappings")
    editor.geometry(f"400x375+{x+600}+{y}")
    editor.configure(fg_color="#2D2D2D")

    mapping = load_mapping()

    mapping_listbox = CTkTextbox(editor, height=200, width=350)
    mapping_listbox.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10))
    mapping_listbox.configure(state="normal")
    for ext, folder in mapping.items():
        mapping_listbox.insert("end", f"{ext} -> {folder}\n")
    mapping_listbox.configure(state="disabled")

    ext_entry = CTkEntry(editor, placeholder_text=".ext", width=150)
    folder_entry = CTkEntry(editor, placeholder_text="Folder Name", width=150)
    ext_entry.grid(row=1, column=0, padx=10, pady=5)
    folder_entry.grid(row=1, column=1, padx=10, pady=5)


    def add_mapping():
        ext = ext_entry.get().strip().lower()
        folder = folder_entry.get().strip()
        if not ext or not folder:
            return
        
        if ext[0] != ".":
            ext = "." + ext

            def refresh_listbox():
                mapping_listbox.configure(state="normal")
                mapping_listbox.delete("1.0", "end")
                for k, v in mapping.items():
                    mapping_listbox.insert("end", f"{k} -> {v}\n")
                mapping_listbox.configure(state="disabled")


            def save_ext_to_mapping():
                mapping[ext] = folder
                save_mapping(mapping)
                refresh_listbox()
                ext_entry.delete(0, END)
                folder_entry.delete(0, END)
                insert_text(f"Successfully added {ext} to {folder}.")

        
            if ext in mapping:
                mapping_listbox.configure(state="normal")
                mapping_listbox.insert("end", f"{ext} is already in the mapping!\n")
                mapping_listbox.configure(state="disabled")
                confirm_window = CTkToplevel(editor)
                confirm_window.title("Confirm Override")
                confirm_window.geometry(f"300x150+{x+600}+{y+325}")
                confirm_window.grab_set()
                confirm_window.configure(fg_color="#2D2D2D")

                label = CTkLabel(confirm_window, text=f"'{ext}' already exists.\nOverride mapping?", font=("Consolas", 14), text_color="white")
                label.pack(pady=20)

                button_frame = CTkFrame(confirm_window, fg_color="transparent")
                button_frame.pack(pady=10)

                yes_button = CTkButton(button_frame, text="Yes", command=lambda: (save_ext_to_mapping(), confirm_window.destroy()), fg_color="#4CAF50")
                no_button = CTkButton(button_frame, text="No", command=confirm_window.destroy, fg_color="#F44336")

                yes_button.grid(row=0, column=0, padx=10)
                no_button.grid(row=0, column=1, padx=10)
            else:
                save_ext_to_mapping()


    def clear_all():
        mapping.clear()
        save_mapping(mapping)
        mapping_listbox.configure(state="normal")
        mapping_listbox.delete("1.0", "end")
        mapping_listbox.configure(state="disabled")
        insert_text("Successfully cleared all items.")

    add_button = CTkButton(editor, text="Add / Update", command=add_mapping)
    clear_button = CTkButton(editor, text="Clear All", command=clear_all, fg_color="#AA4444", hover_color="#BB5555")

    add_button.grid(row=2, column=0, padx=10, pady=10)
    clear_button.grid(row=2, column=1, padx=10, pady=10)


    def remove_mapping():
        ext = ext_entry.get().strip().lower()
        if not ext:
            return
        if not ext.startswith("."):
            ext = "." + ext
        if ext in mapping:
            del mapping[ext]
            save_mapping(mapping)
            mapping_listbox.configure(state="normal")
            mapping_listbox.delete("1.0", "end")
            for k, v in mapping.items():
                mapping_listbox.insert("end", f"{k} -> {v}\n")
            mapping_listbox.configure(state="disabled")
            ext_entry.delete(0, END)
            folder_entry.delete(0, END)
            insert_text(f"Successfully removed mapping for {ext}.\n")
        else:
            insert_text(f"No mapping found for {ext}.\n")

    remove_button = CTkButton(editor, text="Remove", command=remove_mapping, fg_color="#FFA500", hover_color="#FFB347")
    remove_button.grid(row=3, column=0, columnspan=2, padx=10, pady=(5, 15), sticky="ew")


def organizeFolder(path: str):
    try:
        if path[-1] != "/":
            path = path+"/"

        files = os.listdir(path)
        file_extensions = [os.path.splitext(file)[1] for file in files]
        file_extensions = [item for item in file_extensions if item.strip()]
        organization = load_mapping()

        for i, file in enumerate(files):
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext == "":
                continue

            dest_folder = organization.get(file_ext, "Miscellaneous")
            dest_path = os.path.join(path, dest_folder)

            if not os.path.isdir(dest_path):
                os.makedirs(dest_path)

            try:
                shutil.move(os.path.join(path, file), dest_path)
                insert_text(f"Moved: {file} -> {dest_folder}\n")
            except Exception as e:
                insert_text(f"Error moving {file}: {e}\n")

            insert_text(f"Finished {i + 1}/{len(files)}\n")

        insert_text("Organization complete!\n")
    except IndexError:
        insert_text("Empty Input!\n")

        
app = CTk()
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
width = 600
height = 475

x = int((screen_width / 2) - (width / 2))
y = int((screen_height / 2) - (height / 2))

app.geometry(f"{width}x{height}+{x}+{y}")
app.resizable(False, False)
app.title("Folder Organizer")
app.configure(fg_color="#242425")

for i in range(2):
    app.grid_columnconfigure(i, weight=1)

app.grid_rowconfigure(4, weight=1)

textbox = CTkEntry(master=app, width=390, height=75, corner_radius=25, border_width=2, border_color="#000000", text_color="#FFFFFF", font=CTkFont(family="San Francisco", size=14), fg_color="#3F69A1", bg_color="#242425")
textbox.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

button = CTkButton(app, text="Submit", command=button_event)
button.grid(row=1, column=0, padx=(10, 5), pady=(5, 5), sticky="e")

button1 = CTkButton(app, text="Select Folder", command=selectfile)
button1.grid(row=1, column=1, padx=(5, 10), pady=(5, 5), sticky="w")

label = CTkLabel(app, text="Action Logs", font=("Consolas", 20), fg_color="#FFFFFF", width=150, corner_radius=10)
label.grid(row=2, column=0, columnspan=2, pady=(10, 0))

logger = CTkTextbox(master = app, width = 600, height = 250, corner_radius = 25, border_width = 2, fg_color = "#0C0C0C", text_color = "#FFFFFF", font = CTkFont(family="San Francisco", size=11))
logger.grid(row=3, column=0, columnspan=2, padx=10, pady=(5, 10), sticky="nsew")

bottom_button = CTkButton(app, text="Edit File Mappings", command=lambda: open_mapping_editor())
bottom_button.grid(row=4, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

app.mainloop()
