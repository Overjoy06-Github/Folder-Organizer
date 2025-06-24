import os
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


app = CTk()
app.geometry("600x435")
app.title("Folder Organizer")
app.configure(fg_color="#242425")

textbox = CTkEntry(master=app, width=390, height=75, corner_radius=25, border_width=2, border_color="#000000", text_color="#FFFFFF", font=CTkFont(family="San Francisco", size=14), fg_color="#3F69A1", bg_color="#242425")
logger = CTkTextbox(master = app, width = 600, height = 250, corner_radius = 25, border_width = 2, fg_color = "#0C0C0C", text_color = "#FFFFFF", font = CTkFont(family="San Francisco", size=11))

label = CTkLabel(app, text="Action Logs", font=("Consolas", 20), fg_color="#FFFFFF", width=150, corner_radius=10)
button = CTkButton(app, text="Submit", command=button_event)
button1 = CTkButton(app, text="Select Folder", command=selectfile)

textbox.place(relwidth=1)
label.place(x=95, y=150, anchor="center")
logger.place(x=300, y=290, anchor="center")
button.place(x=225, y=100, anchor="center")
button1.place(x=375, y=100, anchor="center")


def insert_text(text):
    logger.configure(state="normal")
    logger.insert("end", text)
    logger.see("end")
    logger.configure(state="disabled")


def organizeFolder(path: str):
    try:
        if path[-1] != "/":
            path = path+"/"

        files = os.listdir(path)
        file_extensions = [os.path.splitext(file)[1] for file in files]
        file_extensions = [item for item in file_extensions if item.strip()]
        organization = {
            ".jpg": "Images",
            ".png": "Images",
            ".gif": "Images",
            ".jfif": "Images",
            ".txt": "Documents",
            ".zip": "Archives",
            ".exe": "Applications",
            ".py": "Python",
            ".mp3": "Audio",
            ".m4a": "Audio"
        }

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


app.mainloop()
