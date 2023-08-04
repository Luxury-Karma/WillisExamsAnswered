import tkinter as tk
from tkinter import messagebox
import json

def on_entry_click(event):
    widget = event.widget
    if widget.get() == widget.placeholder:
        widget.delete(0, tk.END)
        widget.config(fg = 'black')

def on_focusout(event):
    widget = event.widget
    if widget.get() == '':
        widget.insert(0, widget.placeholder)
        widget.config(fg = 'grey')

def get_entry_data(entry):
    return entry.get()

def create_entry(parent, placeholder):
    entry = tk.Entry(parent)
    entry.placeholder = placeholder
    entry.insert(0, entry.placeholder)
    entry.bind('<FocusIn>', on_entry_click)
    entry.bind('<FocusOut>', on_focusout)
    entry.config(fg = 'grey')
    return entry

def open_settings(settings, root):
    frame = settings.get("frame")
    if frame is not None:
        frame.destroy()
        settings["frame"] = None
    else:
        frame = tk.Frame(root, bd=1, relief='sunken')
        frame.pack(side=tk.LEFT, fill=tk.Y)

        user_button = tk.Button(frame, text="User", command=lambda: print("User button clicked"))
        user_button.pack(fill=tk.X)

        browser_button = tk.Button(frame, text="Browser", command=lambda: print("Browser button clicked"))
        browser_button.pack(fill=tk.X)

        new_db_button = tk.Button(frame, text="New DB", command=lambda: print("New DB button clicked"))
        new_db_button.pack(fill=tk.X)

        settings["frame"] = frame

def run_search(quix_url_entry, quiz_cours_entry, search_entry, table_entry):
    quix_url = get_entry_data(quix_url_entry)
    quiz_course = get_entry_data(quiz_cours_entry)
    search_text = get_entry_data(search_entry)
    # todo make it fill table
    # assuming that you have some JSON data to fill the table
    json_data = ["Item1", "Item2", "Item3"]
    fill_table_with_json(table_entry, json_data)

    print(f"Quix URL: {quix_url}, Quiz Course: {quiz_course}, Search Text: {search_text}")

def fill_table_with_json(table, json_data):
    # Clear the table before inserting new data
    table.delete(0, tk.END)

    for item in json_data:
        table.insert(tk.END, item)

def setup_ui(root):
    root.geometry('800x600')

    navbar = tk.Frame(root)
    navbar.pack(side=tk.TOP, fill=tk.X)

    settings = {"frame": None}

    setting_button = tk.Button(navbar, text="Settings", command=lambda: open_settings(settings, root))
    snapmode_button = tk.Button(navbar, text="Snapmode", command=lambda: print("Snapmode button clicked")) # Todo : Call Snap mode ( picture )

    setting_button.pack(side=tk.LEFT, fill=tk.X)
    snapmode_button.pack(side=tk.LEFT, fill=tk.X)

    main_body = tk.Frame(root)
    main_body.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    quix_url_entry = create_entry(main_body, "Enter quix URL")
    quiz_cours_entry = create_entry(main_body, "Enter quiz course")
    search_entry = create_entry(main_body, "Search")

    quix_url_entry.grid(row=0, column=0, sticky='ew')
    quiz_cours_entry.grid(row=0, column=1, sticky='ew')
    search_entry.grid(row=1, column=0, sticky='ew')

    table = tk.Listbox(main_body)
    table.grid(row=2, column=0, columnspan=2, sticky='nsew')

    search_button = tk.Button(main_body, text="Search", command=lambda: run_search(quix_url_entry, quiz_cours_entry, search_entry, table))  # Todo : add link to table ( reference ) and modify data dynamicly
    search_button.grid(row=1, column=1, sticky='ew')

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)



    main_body.grid_columnconfigure(0, weight=1)
    main_body.grid_columnconfigure(1, weight=1)
    main_body.grid_rowconfigure(2, weight=1)



def main():
    root = tk.Tk()
    setup_ui(root)
    root.mainloop()

if __name__ == "__main__":
    main()
