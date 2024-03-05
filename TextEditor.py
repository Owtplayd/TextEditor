import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import ttk, font

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")
        self.root.geometry("800x600")  # Set the initial size for the window
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # text window
        self.text_edit = tk.Text(root, font=("TimesNewRoman", 14), fg="black", bg="white", wrap="word", undo=True)
        self.text_edit.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Create a frame for font and font size dropdowns
        self.font_frame = tk.Frame(root)
        self.font_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Create a list of available fonts
        fonts = list(font.families())
        fonts.sort()

        # Default font
        self.selected_font_var = tk.StringVar(value="TimesNewRoman")

        # Dropdown menu for font
        self.font_menu = ttk.Combobox(self.font_frame, textvariable=self.selected_font_var, values=fonts, state="readonly", width=15)
        self.font_menu.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Create a list of available font sizes
        font_sizes = list(range(8, 31))  # You can adjust the range based on your preference

        # Default font size
        self.selected_size_var = tk.StringVar(value="14")

        # Dropdown menu for font size
        self.size_menu = ttk.Combobox(self.font_frame, textvariable=self.selected_size_var, values=font_sizes, state="readonly", width=5)
        self.size_menu.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Bind the <FocusOut> event to the change_font and change_font_size functions
        self.font_menu.bind("<FocusOut>", self.change_font)
        self.size_menu.bind("<FocusOut>", self.change_font_size)

        # Create a frame for file buttons
        self.file_frame = tk.Frame(root, relief=tk.RAISED, bd=2)
        self.file_frame.grid(row=1, column=0, columnspan=2, sticky="ew")

        # "Save" button
        self.save_button = tk.Button(self.file_frame, text="Save", command=self.save_file)
        self.save_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # "Open" button
        self.open_button = tk.Button(self.file_frame, text="Open", command=self.open_file)
        self.open_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # "Undo" button
        self.undo_button = tk.Button(self.file_frame, text="Undo", command=self.undo_action)
        self.undo_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # "Redo" button
        self.redo_button = tk.Button(self.file_frame, text="Redo", command=self.redo_action)
        self.redo_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Bind Ctrl+Z to undo and Ctrl+Y to redo
        root.bind("<Control-z>", self.undo_action)
        root.bind("<Control-y>", self.redo_action)

        # Initialize history and redo history as empty lists
        self.history = []
        self.redo_history = []

        # Add a binding to track changes in the text
        self.text_edit.bind("<Key>", self.track_changes)

    def track_changes(self, event):
        # Track text changes and update history
        change = {"action": event.char, "index": self.text_edit.index(tk.INSERT)}
        self.history.append(change)
        # Clear redo history when a new change is made
        self.redo_history = []

    def undo_action(self, event=None):
        if self.history:
            # Get the most recent change
            last_change = self.history.pop()
            # Add the change to the redo history
            self.redo_history.append(last_change)
            # Disable undo events temporarily to prevent re-tracking
            self.text_edit.edit_separator()
            self.text_edit.edit_undo()
            # Re-enable undo events
            self.text_edit.edit_separator()

    def redo_action(self, event=None):
        if self.redo_history:
            # Get the most recent undone change
            undone_change = self.redo_history.pop()
            # Add the change back to the history
            self.history.append(undone_change)
            # Disable undo events temporarily to prevent re-tracking
            self.text_edit.edit_separator()
            # Apply the undone change
            self.text_edit.edit_redo()
            # Re-enable undo events
            self.text_edit.edit_separator()

    def open_file(self):
        filepath = askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not filepath:
            return
        self.text_edit.delete(1.0, tk.END)
        with open(filepath, "r") as f:
            content = f.read()
            self.text_edit.insert(tk.END, content)
        self.root.title(f"Open file: {filepath}")

    def save_file(self):
        filepath = asksaveasfilename(filetypes=[("Text Files", "*.txt")])
        if not filepath:
            return
        with open(filepath, "w") as f:
            content = self.text_edit.get(1.0, tk.END)
            f.write(content)
        self.root.title(f"Save file: {filepath}")

    def change_font(self, event=None):
        selected_font = self.selected_font_var.get()
        self.text_edit.configure(font=(selected_font, int(self.selected_size_var.get())))

    def change_font_size(self, event=None):
        self.text_edit.configure(font=(self.selected_font_var.get(), int(self.selected_size_var.get())))

if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()